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
from os.path import abspath, dirname
from sys import path

SITE_ROOT = dirname(dirname(abspath(__file__)))
path.insert(0, SITE_ROOT)

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "jajaja.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HedyNet.settings.development")

environment_settings = (
    "DJANGO_SETTINGS_MODULE",
    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "SECRET_KEY",
    "EMAIL_ACCOUNT",
    "EMAIL_PASSWORD",
)

def application(environ, start_response):

    if "VIRTUALENV_PATH" in environ:
        path.insert(0, environ["VIRTUALENV_PATH"])

    for key in environment_settings:
        if key in environ:
            os.environ[key] = str(environ[key])

    import django.core.handlers.wsgi
    _application = django.core.handlers.wsgi.WSGIHandler()

    return _application(environ, start_response)
