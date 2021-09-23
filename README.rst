=====
Heading
=====
Django Google Drive Personal Storage

Detailed documentation is in the "docs" directory.
Quick start
-----------
1. Add "gdpstorage" to your INSTALLED_APPS setting like this::
INSTALLED_APPS = [
        ...
        'gdpstorage',
    ]

2. Include the polls URLconf in your project urls.py like this::
path('gdps/', include('gdpstorage.urls'))
