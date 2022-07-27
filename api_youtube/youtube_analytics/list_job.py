import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2.refresh_token import YoutubeToken
from config.cons import CONTENT_OWNER_ID
from youtube_analytics.create_job import value_default, remove_empty_kwargs, get_authenticated_service
# Call the YouTube Reporting API's jobs.list method to retrieve reporting jobs.
def list_reporting_jobs(youtube_reporting, **kwargs):
    # Only include the onBehalfOfContentOwner keyword argument if the user
    # set a value for the --content_owner argument.
    kwargs = remove_empty_kwargs(**kwargs)

    # Retrieve the reporting jobs for the user (or content owner).
    results = youtube_reporting.jobs().list(**kwargs).execute()

    if 'jobs' in results and results['jobs']:
        jobs = results['jobs']
        for job in jobs:
            print(f"Reporting job id: {job['id']}\n name: {job['name']}\n for reporting type: {job['reportTypeId']}\n")
    else:
        print('No jobs found')
        return False

    return True

# Call the YouTube Reporting API's reports.list method to retrieve reports created by a job.
def retrieve_reports(youtube_reporting, **kwargs):
    # Only include the onBehalfOfContentOwner keyword argument if the user
    kwargs = remove_empty_kwargs(**kwargs)

    # Retrieve available reports for the selected job.
    results = youtube_reporting.jobs().reports().list(**kwargs).execute()

    if 'reports' in results and results['reports']:
        reports = results['reports']
        for report in reports:
            print (f"Report dates: {report['startTime']} to {report['endTime']}\ndownload URL: {report['downloadUrl']}\n")


def list_jobs():
    youtube_reporting = get_authenticated_service()
    try:
        # If the user has not specified a job ID or report URL, retrieve a list
        # of available jobs and prompt the user to select one.
        list_reporting_jobs(youtube_reporting, onBehalfOfContentOwner=CONTENT_OWNER_ID)

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
