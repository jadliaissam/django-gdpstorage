import os

from pydrive2.auth import GoogleAuth

CLIENT_SECRETS_FILE_PATH = "credentials.json"


def load_credentials_from_env():
    CLIENT_SECRETS_FROM_ENV = os.environ.get('CLIENT_SECRETS_FROM_ENV', 0)
    CLIENT_SECRETS_FILE_CONTENT = os.environ.get('CLIENT_SECRETS_FILE_CONTENT', '')
    if int(CLIENT_SECRETS_FROM_ENV):
        # We are hosted probably in Heroku
        with open(CLIENT_SECRETS_FILE_PATH, 'wt') as json_file:
            json_file.write(CLIENT_SECRETS_FILE_CONTENT)


def initialize_flow():
    gauth = GoogleAuth()
    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})
    load_credentials_from_env()
    return gauth


def authorize_gd():
    gauth = initialize_flow()
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(CLIENT_SECRETS_FILE_PATH)
    return gauth


def renew_authorize_gd():
    gauth = initialize_flow()
    gauth.LocalWebserverAuth()
    if gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(CLIENT_SECRETS_FILE_PATH)
    return gauth
