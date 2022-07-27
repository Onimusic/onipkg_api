import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd
from io import FileIO
from oauth2.refresh_token import YoutubeToken
from config.cons import CONTENT_OWNER_ID , TABLE_SCHEMA_YT_ANALYTICS, NAME2JOB_ID,\
PLAYBACK_LOCATION_TYPE, TRAFFIC_SOURCE_TYPE, DEVICE_TYPE, OS, AD_TYPE, TABLE_SCHEMA_REPORT
import datetime
import pandas_gbq
from google.oauth2 import service_account
from youtube_analytics.create_job import get_authenticated_service

CLIENT_SECRETS_FILE = 'auth/token.json'
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubereporting'
API_VERSION = 'v1'


class ReportsPeriod:
    def __init__(self, start_date, end_date):
        self.start_date = f'{start_date}T07:00:00Z'
        self.end_date = f'{end_date}T07:00:00Z'
        self.local_file = None
        self.report_url = None

    # Call the YouTube Reporting API's jobs.list method to retrieve reporting jobs.
    def list_reporting_jobs(self, youtube_reporting):
        # Retrieve the reporting jobs for the user (or content owner).
        results = youtube_reporting.jobs().list(
            jobId=self.job_id,
            onBehalfOfContentOwner=CONTENT_OWNER_ID,
            startTimeAtOrAfter=self.start_date,
            startTimeBefore=self.end_date).execute()

        if 'jobs' in results and results['jobs']:
            jobs = results['jobs']
            for job in jobs:
                print (f"Reporting job id: {job['id']}\n name: {job['name']}\n for reporting type:"
                       f" {job['reportTypeId']}\n")
        else:
            print('No jobs found')
            return False

        return True

    def period_reports(self, df_ids, report_name):
        df_concat_days = pd.DataFrame()
        start_date_all = []
        create_time_all = []
        # Only include the onBehalfOfContentOwner keyword argument if the user

        # Retrieve available reports for the selected job.
        youtube_reporting = get_authenticated_service()
        results = youtube_reporting.jobs().reports().list(
            jobId=NAME2JOB_ID[report_name],
            onBehalfOfContentOwner=CONTENT_OWNER_ID,
            startTimeAtOrAfter=self.start_date,
            startTimeBefore=self.end_date
        ).execute()
        if 'reports' in results and results['reports']:
            reports = results['reports']
            #Ordenar por startTime
            print(reports)
            reports.sort(key=lambda x: x['startTime'])
            for idx, report in enumerate(reports):
                start_date_report = report['startTime'].split('T')[0]
                start_date_report = datetime.datetime.strptime(start_date_report, '%Y-%m-%d')
                create_time = report['createTime'].split('.')[0]
                create_time = datetime.datetime.strptime(create_time, '%Y-%m-%dT%H:%M:%S')
                if start_date_report in start_date_all:
                    if create_time < create_time_all[start_date_all.index(start_date_report)]:
                        print(f'Item mantido: {reports[start_date_all.index(start_date_report)]}')
                        print(f'Item removido: {reports[reports.index(report)]}')
                        del reports[reports.index(report)]
                    else:
                        print(f'Item mantido: {reports[reports.index(report)]}')
                        print(f'Item removido: {reports[start_date_all.index(start_date_report)]}')
                        del reports[start_date_all.index(start_date_report)]
                start_date_all.append(start_date_report)
                create_time_all.append(create_time)

            for report in reports:
                start_time = report['startTime'].split('T')[0]
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
                self.report_url = report['downloadUrl']
                self.local_file = f"{report_name}_{start_time}.csv"
                self.download_report(youtube_reporting)
                print(f"Downloaded report for {report['startTime']}")
                df_today = pd.read_csv(self.local_file)
                os.remove(self.local_file)

                df_concat_days = pd.concat([df_concat_days, df_today], ignore_index=True)
            df_concat_days = df_concat_days.merge(df_ids, on='video_id', how='inner')
            if report_name == 'os_device_tf_source':
                df_concat_days['playback_location_type'] = df_concat_days['playback_location_type'].apply(
                    lambda val: PLAYBACK_LOCATION_TYPE[str(val)])
                df_concat_days['traffic_source_type'] = df_concat_days['traffic_source_type'].apply(
                    lambda val: TRAFFIC_SOURCE_TYPE[str(val)])
                df_concat_days['device_type'] = df_concat_days['device_type'].apply(lambda val: DEVICE_TYPE[str(val)])
                df_concat_days['operating_system'] = df_concat_days['operating_system'].apply(lambda val: OS[str(val)])
                df_out = df_concat_days.groupby(
                    ['video_id', 'channel_id', 'title', 'date', 'subscribed_status', 'live_or_on_demand',
                     'country_code', 'playback_location_type', 'traffic_source_type', 'device_type',
                     'operating_system'], as_index=False).sum()[
                    ['video_id', 'channel_id', 'title', 'date', 'subscribed_status', 'live_or_on_demand',
                     'country_code', 'playback_location_type', 'traffic_source_type', 'device_type', 'operating_system',
                     'views', 'watch_time_minutes', 'red_views', 'red_watch_time_minutes']]

                df_out['average_view_duration_seconds'] = df_out['watch_time_minutes'] * 60 / df_out['views']
                df_out['red_average_view_duration'] = df_out['red_watch_time_minutes'] * 60 / df_out['red_views']
                df_out.drop(['red_watch_time_minutes', 'watch_time_minutes'], axis=1, inplace=True)


            elif report_name == 'basic':
                df_out = df_concat_days.groupby(['video_id', 'date', 'subscribed_status', 'country_code'],
                                                as_index=False).sum()[
                    ['video_id', 'date', 'subscribed_status', 'country_code', 'likes', 'dislikes', 'comments', 'shares',
                     'subscribers_gained', 'subscribers_lost', 'videos_added_to_playlists',
                     'videos_removed_from_playlists']]
            elif report_name == 'ad_revenue':
                df_out = df_concat_days.copy()
                df_out['ad_type'] = df_out['ad_type'].apply(lambda val: AD_TYPE[str(val)])
            elif report_name == 'all_revenue':
                df_out = df_concat_days.copy()

            df_out['date'] = pd.to_datetime(df_out['date'], format='%Y%m%d')
            df_out.dropna(subset=['video_id'], inplace=True)
        return df_out

    def get_basic_df(self, df_ids):
        df_basic = self.period_reports(df_ids, 'basic')
        return df_basic

    def get_os_device_tf_source_df(self, df_ids):
        df_os_device_tf_source = self.period_reports(df_ids, 'os_device_tf_source')
        return df_os_device_tf_source

    def get_ad_revenue_df(self, df_ids):
        df_ad_revenue = self.period_reports(df_ids, 'ad_revenue')
        return df_ad_revenue

    def get_all_revenue_df(self, df_ids):
        df_all_revenue = self.period_reports(df_ids, 'all_revenue')
        return df_all_revenue



    # Call the YouTube Reporting API's media.download method to download the report.
    def download_report(self, youtube_reporting):
        request = youtube_reporting.media().download(
            resourceName=' '
        )
        request.uri = self.report_url
        fh = FileIO(self.local_file, mode='wb')
        # Stream/download the report in a single request.
        downloader = MediaIoBaseDownload(fh, request, chunksize=-1)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download {int(status.progress() * 100)}%%.")
        print('Download Complete!')


    # Prompt the user to select a job and return the specified ID.
    def get_job_id_from_user(self):
        job_id = input('Please enter the job id for the report retrieval: ')
        print (f"You chose {job_id} as the job Id for the report retrieval.")
        return job_id

    # Prompt the user to select a report URL and return the specified URL.
    def get_report_url_from_user(self):
        report_url = input('Please enter the report URL to download: ')
        print (f'You chose {report_url} to download.')
        return report_url

    def get_list_reports(self):
        youtube_reporting = get_authenticated_service()
        try:
            if not self.job_id and not self.report_url:
                if self.list_reporting_jobs(youtube_reporting):
                    self.job_id = self.get_job_id_from_user()
            elif self.job_id and not self.report_url:
                self.period_reports()
                self.report_url = self.get_report_url_from_user()
            else:
                self.download_report(youtube_reporting)
        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')


