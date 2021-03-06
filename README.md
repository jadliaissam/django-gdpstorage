# Google Drive Personal Storage for Django
GDPS is a django app to provide Google Drive as a Storage Backeend for Django Project.
It can be used to store the files in the user space (visible in the Web UI of Google Drive) while other librairies propose the use of Google Cloud Project to achieve the same results (with the downside of not being able to see the uploaded files).

## Features
- Use your Personal Google Cloud Folder as a Storage Backend.
- Few views are added for Authorization with Google Drive and its renew (if you decide later to change the Google Account used).
- For convenience, few abstract models (abstract and on-demande obvisouly)  are provided to add the functionnality of SoftDeletion to your project (which is important if you are manipulationg Files).

## Inspiration
This package was hugely inspired by :
- @torre76 excellent package : https://github.com/torre76/django-googledrive-storage
- @iterative excellent package : https://github.com/iterative/PyDrive2

## Installation
    pip install gdpstorage

## Setup
-Add "gdpstorage" to your INSTALLED_APPS setting like this :
```py
    INSTALLED_APPS = [
        ...
        'gdpstorage',
    ]
```
-Include the gdpstorage's URLconf in your project urls.py like this:
```py
path('gdps/', include('gdpstorage.urls'))
```
-Add The following settings to your settings.py :
```py
# Replace [MY-GD-FOLDERNAME] by the name of your Google Drive Folder you wish to use as root Media folder.
GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = "MY-GD-FOLDERNAME"
```
-Change your Default Storage Engine (if you want to use GD globaly, else you can change it on field basis using the storage keyword argument )
```py
DEFAULT_FILE_STORAGE = "gdpstorage.storage.GoogleDriveStorage"
```
-Create your Oath2 application and download your client_secrets.json file (see https://github.com/torre76/django-googledrive-storage documentation for steps )
-Put your file client_secrets.json at the root of your Django project (beside manage.py)
-Authorize the access to your Google Drive Folder by visiting:
    ```sh
    http://127.0.0.1:8000/gdps/authorize
    ```
## Development

Want to contribute? Great!
Feel free to make a pull request or post any issues in the Github repo.
https://github.com/jadliaissam/django-gdpstorage

## License

MIT
