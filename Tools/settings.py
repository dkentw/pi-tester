# Django settings for apt_service project.
# BEGIN <APT setting> ================================================================

# mock classes
from aptlib.mock_kb import MockAPTKB
from aptlib.mock_cache import MockNoCache

from aptlib.aptkb import APTKB
from aptlib.permission import Permission
from aptlib.cache import APTMemCache


MOCK_APTKB_SETTING = {
        'class': MockAPTKB,
        'connection': {}
}
# example for real APTKB
#APTKB_SETTING = {
#    'class': APTKB,
#    'connection': {
#        'host': 'apt-kbcluster01',
#        'port': 27017,
#        'max_pool_size': 50,
#        'network_timeout': 5, #timeout (in seconds) to use for socket operations.
#        'socketTimeoutMS': 1, #How long a send or receive on a socket can take before timing out.
#        'connectTimeoutMS': 0.5, #How long a connection can take to be opened before timing out.
#    }
#}

APTKB_SETTING = {
    'class': APTKB,
    'user_db_class': Permission,
    'connection': {
        'master': ('apt-kbcluster01.sjdc', 27017),
        'slaves': [('apt-kbcluster01', 27017), ('apt-kbcluster02', 27017)],
        'network_timeout': 1,
        'dbname': 'graph',
        'user_dbname': 'user',
        'node_collection_name': 'nodes',
        'perm_collection_name': 'permission',
    }
    
#    'connection': {
#        #'mongo_addr': ('10.1.147.57', 27017),
#        'type': 'single'
#        'host': 'apt-kbcluster01',
#        'port': 27017,
#        'network_timeout': 1,
#        'dbname': 'graph',
#        'user_dbname': 'user',
#        'node_collection_name': 'nodes',
#        'perm_collection_name': 'permission',
#    }
}

APT_USER_DB_SETTING = APTKB_SETTING 

APT_CACHE_SETTING = {
    'class': APTMemCache,
    'connection': {
        # [(<server:port>, <server_weight>), ...]
        'servers': [('apt-cache01:6379', 1000), ('apt-cache02:6379', 1000)],
        'debug': 1,
    }
}

MOCK_APT_NO_CACHE = {
    'class': MockNoCache,
    'connection': {}
}

APT_SERVICE_SETTINGS = {
    #'aptkb': MOCK_APTKB_SETTING,
    'aptkb': APTKB_SETTING,
    'user_db': APT_USER_DB_SETTING,
    #'aptcache': MOCK_APT_NO_CACHE,
    'aptcache': APT_CACHE_SETTING,
    #'normal_ttl': 60*60,
    #'negative_tll': 60*60,
}


APT_CACHE_TTL = 60*60             # seconds
APT_NEGATIVE_CACHE_TTL = 60*60*24 # seconds

APT_USER_DB_CACHE_TTL = 60*60             # seconds
APT_USER_DB_NEGATIVE_CACHE_TTL = 60*60*24 # seconds

APT_RESPONSE_TTL = APT_CACHE_TTL


def get_aptkb(username, password):
    setting = APT_SERVICE_SETTINGS['aptkb'] 
    return setting['class'](username, password, setting['connection'])

def get_user_db():
    setting = APT_SERVICE_SETTINGS['user_db']
    return setting['user_db_class'](setting['connection'])

def get_aptcache():
    setting = APT_SERVICE_SETTINGS['aptcache']
    return setting['class'](setting['connection'])

# END   <APT setting> ================================================================

DEBUG = False
#TEMPLATE_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG

"""
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
"""
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
"""
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

#SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
#STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#)

# List of finder classes that know how to find static files in
# various locations.
#STATICFILES_FINDERS = (
    #'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
#)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a8sn$56w5tjcb)q0b2%qscds^$rsv3o7$4#1fz^k+#4xuo#@u6'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
    #'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
#)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    #os.path.join(SITE_ROOT, 'templates')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
