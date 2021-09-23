from django.urls import path

from .views import authorize_google_drive_access, renew_google_drive_access, get_oath_client_secrets

urlpatterns = [
    path('authorize', authorize_google_drive_access),
    path('renew', renew_google_drive_access),
    path('file', get_oath_client_secrets),
]
