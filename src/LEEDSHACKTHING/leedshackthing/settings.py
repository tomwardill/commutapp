# $Id$

# Base settings
__author__ = 'Forename Surname <forename@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_STATIC = True

ADMINS = (
    ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'leedshack',                      # Or path to database file if using sqlite3.
        'USER': 'leedshack',                      # Not used with sqlite3.
        'PASSWORD': 'password',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Calculated site root
PATH_SITE_ROOT = os.path.normpath(os.path.dirname(__file__))

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PATH_SITE_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z5(1^cw^^q9s0m^-o2j^(2npq1(b*n62!*#p_vajm_0kvh_se8'

# Email sent from the server (debug stack traces, etc) will use this address
SERVER_EMAIL = 'root@localhost'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(PATH_SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.gis',
    'leedshackthing.main',
    'south',
    'djcelery'
)

import djcelery
djcelery.setup_loader()

ROOT_URLCONF = 'leedshackthing.urls'

DATA_URLS = {
    'currentroad': 'http://datex2.tistrafficinfo.com/England/CurrentPlanned/content.xml'
    }

TRAFFIC_USERNAME = 'twardill'
TRAFFIC_PASSWORD = ''
LOCAL_DATA = False
LOGIN_REDIRECT_URL = '/'
AUTH_PROFILE_MODULE = "main.UserProfile"
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Celery settings
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"


from datetime import timedelta
# Celery scheduled tasks
CELERYBEAT_SCHEDULE = {
    "import-current-road": {
        "task": "leedshackthing.main.tasks.update_current_road",
        "schedule": timedelta(minutes = 15),
        },
    "import-future-road": {
        "task": "leedshackthing.main.tasks.update_future_road",
        "schedule": timedelta(hours = 6),
        },
    "import-unplanned-events": {
        "task": "leedshackthing.main.tasks.update_unplanned_events",
        "schedule": timedelta(minutes = 10),
        },
    }


# Override with environment specific settings
try:
    from local_settings import *
except ImportError:
    pass
