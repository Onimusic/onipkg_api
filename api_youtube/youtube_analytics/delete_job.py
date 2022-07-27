import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2.refresh_token import YoutubeToken
from config.cons import CONTENT_OWNER_ID
from youtube_analytics.create_job import value_default, remove_empty_kwargs, get_authenticated_service
# Authorize the request and store authorization credentials.
# Call the YouTube Reporting API's jobs.create method to create a job.

def delete_reporting_job(youtube_reporting, job_id, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    reporting_job = youtube_reporting.jobs().delete(jobId=job_id, **kwargs).execute()
    print(f"Deleted the report_job: {job_id}")



def delete_job():
    job_id = input('Please set a job id: ')
    job_id = value_default(job_id, None)
    youtube_reporting = get_authenticated_service()
    try:
        # Prompt user to select report type if they didn't set one on command line.
        # Delete the job.
        delete_reporting_job(youtube_reporting, job_id, onBehalfOfContentOwner=CONTENT_OWNER_ID)
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n {e.content}')
