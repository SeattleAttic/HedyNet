HedyNet
=======

This is the repository for a makerspace management system for Seattle Attic.

It is written in Django, with a default setup of Django/Apache/MySQL.

Installation
============

This set up requires certain environment variables to be set.  The list
can be found in the HedyNet/HedyNet/wsgi.py file.

Best practices involve using virtualenv.  Then, one can:

 pip install -r requirements/local.txt

To install the necessary Python dependencies.  The virtualenv environment
will also need those environment variables to be set in this environment file:

 bin/postactivate

Additionally, in order to compile the SCSS into CSS, Ruby is required with the
following gems installed:

  gem install zurb-foundation
  gem install compass

If you are using apache, there is an example config in HedyNet/apache.

Collecting Static Files
=======================

Do these commands from the base HedyNet directory.

First, one can use Django's collectstatic:

  ./manage.py collectstatic

Then in the HedyNet directory, one can use:

  compass compile

To do a single compile, or:

  compass watch

To continually watch the SCSS files for changes and recompile.
