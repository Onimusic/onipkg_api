import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2.refresh_token import YoutubeToken
from config.cons import CONTENT_OWNER_ID

CLIENT_SECRETS_FILE = 'token.json'

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubereporting'
API_VERSION = 'v1'
# Authorize the request and store authorization credentials.
def get_authenticated_service():
    ytb_token = YoutubeToken()
    credentials = ytb_token.get_creds_analytics()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# Remove keyword arguments that are not set.
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs

# Call the YouTube Reporting API's reportTypes.list method to retrieve report types.
def list_report_types(youtube_reporting, **kwargs):
    # Provide keyword arguments that have values as request parameters.
    kwargs = remove_empty_kwargs(**kwargs)
    results = youtube_reporting.reportTypes().list(**kwargs).execute()
    reportTypes = results['reportTypes']

    if 'reportTypes' in results and results['reportTypes']:
        reportTypes = results['reportTypes']
        for reportType in reportTypes:
            print(f"Report type id: {reportType['id']}\n name: {reportType['name']}\n")
    else:
        print('No report types found')
        return False

    return True


# Call the YouTube Reporting API's jobs.create method to create a job.
def create_reporting_job(youtube_reporting,report_type, name, **kwargs):
    # Provide keyword arguments that have values as request parameters.
    kwargs = remove_empty_kwargs(**kwargs)
    reporting_job = youtube_reporting.jobs().create(body=dict(reportTypeId=report_type,
                                                              name=name), **kwargs).execute()
    print(f"Reporting job {reporting_job['name']} created for reporting type {reporting_job['reportTypeId']} at "
          f"{reporting_job['createTime']}")


# Prompt the user to enter a report type id for the job. Then return the id.
def get_report_type_id_from_user():
    report_type_id = input('Please enter the reportTypeId for the job: ')
    print(f"You chose {report_type_id} as the report type Id for the job.")
    return report_type_id

# Prompt the user to set a job name
def prompt_user_to_set_job_name():
    job_name = input('Please set a name for the job: ')
    print(f"Great! {job_name} is a memorable name for this job.")
    return job_name

def value_default(value, default):
    if not value:
        return default
    else:
        return value

def system_managed_bool(value):
    value = value_default(value, 'n')
    if value == 'y':
        return True
    else:
        return False

def create_job():
    # The 'name' option specifies the name that will be used for the reporting job.
    include_system_managed = input('Do you want to include system managed reports? (y/n): ')
    include_system_managed = system_managed_bool(include_system_managed)
    name = input('Please set a name for the job: ')
    name = value_default(name, None)
    report_type = input('Please enter the reportTypeId for the job: ')
    report_type = value_default(report_type, None)
    youtube_reporting = get_authenticated_service()

    try:
        # Prompt user to select report type if they didn't set one on command line.
        if not report_type:
            if list_report_types(youtube_reporting, onBehalfOfContentOwner=CONTENT_OWNER_ID,
                                 includeSystemManaged=include_system_managed):
                report_type = get_report_type_id_from_user()
        # Prompt user to set job name if not set on command line.
        if not name:
            name = prompt_user_to_set_job_name()
        # Create the job.
        if report_type:
            create_reporting_job(youtube_reporting, report_type, name,
                                 onBehalfOfContentOwner=CONTENT_OWNER_ID)
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n {e.content}')
