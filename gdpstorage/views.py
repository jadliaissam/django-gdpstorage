import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from gdpstorage.gd_service import authorize_gd, renew_authorize_gd, CLIENT_SECRETS_FILE_PATH, CREDENTIALS_FILE_PATH


def authorize_google_drive_access(request):
    authorize_gd()
    return HttpResponse('OAUTH2 Negotiation Ended')


def renew_google_drive_access(request):
    renew_authorize_gd()
    return HttpResponse('Renew OAUTH2 Negotiation Ended')


@user_passes_test(lambda u: u.is_superuser)
def get_oath_client_secrets(request):
    if os.path.exists(CLIENT_SECRETS_FILE_PATH):
        with open(CLIENT_SECRETS_FILE_PATH, 'rt') as json_file:
            return HttpResponse(json_file.read())
    else:
        return HttpResponse('Client Secrets File Not Found !!')


@user_passes_test(lambda u: u.is_superuser)
def get_oath_credentials(request):
    if os.path.exists(CREDENTIALS_FILE_PATH):
        with open(CREDENTIALS_FILE_PATH, 'rt') as json_file:
            return HttpResponse(json_file.read())
    else:
        return HttpResponse('Credentials File Not Found !!')
