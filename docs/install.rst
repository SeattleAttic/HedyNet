Install
=============

Here's what you need to know to get a laptop to run HedyNet locally. The following notes were assembled on a Mac running OSX 10.7.5, Macports, and Python 2.7.1. It assumes you have figured out how to download a copy of HedyNet from github.

Requirements
-----------------
(see the requirements files in the requirements/ folder)

- Pip 
  sudo easy_install pip

- VirtualEnv
  sudo pip install virtualenv

- Django
  venv/bin/pip install django

- Python-dev
  sudo port install python-dev

- Mysql-python (although we're using sqlite3 for local testing)
  sudo port install py27-mysql

Setup More Packages
-----------------
  virtualenv --no-site-packages venv
  ./venv/bin/pip install django
  ./venv/bin/pip install django-braces
  ./venv/bin/pip install django-debug-toolbar
  sudo gem install zurb-foundation (todo: show how to do ruby installations with rvm)
  sudo gem install compass

Configure Django
-----------------
(I had difficulty here and had to resort to the following environment variables. Can someone figure out how to properly load the settings file and make sure the settings reach Django?)

  export DATABASE_ENGINE='django.db.backends.sqlite3'
  export DATABASE_USER=''
  export DATABASE_PASSWORD=''
  export SECRET_KEY="SECRET_KEY"


Initialise Database
-----------------
The following instruction sets up the database (sqlite3) that will store things like user accounts. When it asks, set up a user account

  ./venv/bin/python manage.py syncdb

Generate Styles
-----------------
This site uses Zurb/Foundation to generate styles. To create the style files run:

  compass compile

Issues With This Documentation
-----------------
TODO: At present, the manage.py server option isn't serving static files like stylesheets and so forth. The Apache configuration file includes instructions for Apache and WSGI, but this documentation does need further instructions on making sure that styles and other information is properly made visible for those using manage.py.
