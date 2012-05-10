# Please not, any new attributes you want to add to the settings, please add it to the file global_settings.py
# Set the default value in that file and override the value in this file

import global_settings
from global_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Karthik Abinav', 'karthikabinavs@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'shaastra_2013',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'mojojojo',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MEDIA_ROOT = '/var/www/Alak/'

SITE_URL = 'http://localhost:8000/'

MEDIA_URL = 'http://localhost/ApplicationPortal/'


TEMPLATE_DIRS = (
    '/home/vgtomahawk/Hello-World/Shaastra-2013-Website/template/'

)
