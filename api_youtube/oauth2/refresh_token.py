import json
from google.oauth2 import service_account
import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class YoutubeToken:

    def __init__(self):
        self.client_secrets_file = 'oauth2/secrets.json'
        self.token_file = 'oauth2/token.json'

    def get_creds_analytics(self):
        with open(self.client_secrets_file) as f:
          secrets = json.load(f)
        if os.path.exists(self.token_file):
            token_json = open(self.token_file)
            creds = json.load(token_json)
            self.credentials = google.oauth2.credentials.Credentials(
                        creds['token'],
                        refresh_token=creds['refresh_token'],
                        id_token=creds.get('id_token'),
                        token_uri=creds['token_uri'],
                        client_id=creds['client_id'],
                        client_secret=creds['client_secret'],
                        scopes=creds['scopes'],
                    )
        else:
            self.credentials = None
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print('Refreshing Access Token...')
                self.credentials.refresh(Request())
            else:
                print('Fetching New Tokens...')
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    scopes=['https://www.googleapis.com/auth/yt-analytics.readonly',
                            'https://www.googleapis.com/auth/yt-analytics-monetary.readonly'])
                flow.run_local_server(port=8080, prompt='consent',
                                      authorization_prompt_message='')
                self.credentials = flow.credentials
        return self.credentials

    def write_token(self):
        creds_dict = {'token': self.credentials.token,
                  'refresh_token': self.credentials.refresh_token,
                  'token_uri': self.credentials.token_uri,
                  'client_id': self.credentials.client_id,
                  'client_secret': self.credentials.client_secret,
                  'scopes': self.credentials.scopes}
        # the json file where the output must be stored
        out_file = open("token.json", "w")
        json.dump(creds_dict, out_file)