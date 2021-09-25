import os

from django.core.exceptions import ImproperlyConfigured
from pydrive2.auth import GoogleAuth

CREDENTIALS_FILE_PATH = "credentials.json"
CLIENT_SECRETS_FILE_PATH = "client_secrets.json"


def load_credentials_from_env():
    CLIENT_SECRETS_FILE_CONTENT = os.environ.get('CLIENT_SECRETS_FILE_CONTENT', '')
    CREDENTIALS_FILE_CONTENT = os.environ.get('CREDENTIALS_FILE_CONTENT', '')
    if not os.path.exists(CLIENT_SECRETS_FILE_PATH):
        if CLIENT_SECRETS_FILE_CONTENT:
            with open(CLIENT_SECRETS_FILE_PATH, 'wt') as json_file:
                json_file.write(CLIENT_SECRETS_FILE_CONTENT)
        else:
            raise ImproperlyConfigured("You must provide The content of [client_secrets.json] file "
                                       "in the [CLIENT_SECRETS_FILE_CONTENT] environment variable or"
                                       " the file itself in the Django Root folder")

    if not os.path.exists(CREDENTIALS_FILE_PATH):
        if CREDENTIALS_FILE_CONTENT:
            with open(CREDENTIALS_FILE_PATH, 'wt') as json_file:
                json_file.write(CREDENTIALS_FILE_CONTENT)


def initialize_flow():
    gauth = GoogleAuth()
    load_credentials_from_env()
    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})
    return gauth


def authorize_gd():
    gauth = initialize_flow()
    gauth.LoadCredentialsFile(CREDENTIALS_FILE_PATH)
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
    gauth.SaveCredentialsFile(CREDENTIALS_FILE_PATH)
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
    gauth.SaveCredentialsFile(CREDENTIALS_FILE_PATH)
    return gauth
