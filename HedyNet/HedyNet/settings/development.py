"""Development settings and globals."""

from os.path import join, normpath

from base import *

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    #'debug_toolbar',
    #'django_extensions',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)
########## END TOOLBAR CONFIGURATION

"""
Logging config is a bit tricky; here are some documents on it:
http://docs.python.org/2/library/logging.html
https://docs.djangoproject.com/en/dev/topics/logging/
http://stackoverflow.com/questions/5438642/django-setup-default-logging
"""
DEBUG_LOGFILE = join(dirname(SITE_ROOT), 'logs', 'debug.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'formatter': 'verbose',         # define the formatter to associate
            'filename': DEBUG_LOGFILE,
        },
    },
    'loggers': {
        # catch all logger
        '': {
            'handlers': ['debug_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # django logger; want to be able to control the level easily
        'django': {
            'handlers': ['debug_file'],
            'level': 'INFO',
            'propogate': False,
        },
        'profiles': {
            'handlers': ['debug_file'],
            'propogate': False,
            'level': 'DEBUG',
        }
    }
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False
