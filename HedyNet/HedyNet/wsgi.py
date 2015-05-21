from __future__ import unicode_literals
"""
WSGI config for HedyNet project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
from sys import path
from sys import stderr
from os.path import abspath, dirname

# Need to have the project root available for
# settings importing
SITE_ROOT = dirname(dirname(abspath(__file__)))
path.insert(0, SITE_ROOT)

environment_settings = (
    "DJANGO_SETTINGS_MODULE",
    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "SECRET_KEY",
    "MAILCHIMP_API_KEY",
    "EMAIL_ACCOUNT",
    "EMAIL_PASSWORD",
)

def application(environ, start_response):

    global environment_settings

    if "VIRTUALENV_PATH" in environ:
        addpath = environ["VIRTUALENV_PATH"]
        if not addpath in path:
            print "Adding VIRTUALENV_PATH: %s" % environ["VIRTUALENV_PATH"]
            path.insert(0, environ["VIRTUALENV_PATH"])

    for key in environment_settings:
        if key in environ:
            os.environ[key] = str(environ[key])

    from django.core.wsgi import get_wsgi_application

    _application = get_wsgi_application()

    return _application(environ, start_response)
