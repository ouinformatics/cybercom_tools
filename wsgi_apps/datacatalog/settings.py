# Django settings for example project.

# Handle logging for this project
import logging
import os
import sys
#logging.basicConfig(
#    level = logging.DEBUG,
#    format = '%(asctime)s %(levelname)s [%(name)s] %(message)s',
#)

# These are all optional and set to their default values
#RPC4DJANGO_LOG_REQUESTS_RESPONSES = True
#RPC4DJANGO_RESTRICT_INTROSPECTION = False
#RPC4DJANGO_RESTRICT_JSONRPC = False
#RPC4DJANGO_RESTRICT_XMLRPC = False
#RPC4DJANGO_RESTRICT_METHOD_SUMMARY = False
#RPC4DJANGO_RESTRICT_RPCTEST = False
#RPC4DJANGO_RESTRICT_REST = False
#RPC4DJANGO_RESTRICT_OOTB_AUTH = False
#RPC4DJANGO_HTTP_ACCESS_CREDENTIALS = True
#RPC4DJANGO_HTTP_ACCESS_ALLOW_ORIGIN = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',# sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': 'cybercom', #mstacy home db
        'NAME':'auth',#catalog', # work  fire.rccc.ou.edu
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'fire.rccc.ou.edu',
        #'HOST': '',#mstacy Home settings   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'catalog': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',# sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': 'cybercom', #mstacy home db
        'NAME':'catalog', # work  fire.rccc.ou.edu
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'fire.rccc.ou.edu',
        #'HOST': '',#mstacy Home settings   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}
DATABASE_ROUTERS = ['datacatalog.editCatRouter.editCatRouter']
#DATABASE_ROUTERS = ['editCatRouter.editCatRouter']
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = "cc90e55712bd08830fd3a82adbeb2cfb"
#SECRET_KEY = 'RPC4Django Example -- Super Secret. Shhhhhh'
LOGIN_URL = '/accounts/login/'# '/auth/login.cgi'
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.app_directories.load_template_source',
    #'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'authtkt.middleware.AuthTktMiddleware',
    # Must be enabled for RPC4Django authenticated method calls
    'django.contrib.auth.middleware.AuthenticationMiddleware',
   #'authtkt.middleware.AuthTktMiddleware', 
    # Required for RPC4Django authenticated method calls
    # Also requires Django 1.1+
    #'dataportal.auth_R_User.ProxyRemoteUserMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
)
#django.middleware.common.CommonMiddleware.APPEND_SLASH = True
# Required for RPC4Django authenticated method calls
# Also requires Django 1.1+
#AUTHENTICATION_BACKENDS = (
#    'django.contrib.auth.backends.RemoteUserBackend',
    #'django.contrib.auth.backends.ModelBackend')

ROOT_URLCONF = 'datacatalog.urls'
#ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #"/Users/mstacy/virtpy/dataportal/templates",
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
#    'django.contrib.messages',#add admin
#    'dataportal.testapp',
#    'dataportal.rpcservice',
#    'rpc4django',
    'authtkt',
    'editCat',
)
