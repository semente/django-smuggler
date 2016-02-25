===============
Django Smuggler
===============

.. image:: https://badge.fury.io/py/django-smuggler.svg
    :target: http://badge.fury.io/py/django-smuggler

.. image:: https://travis-ci.org/semente/django-smuggler.svg?branch=master
    :target: https://travis-ci.org/semente/django-smuggler

.. image:: https://coveralls.io/repos/semente/django-smuggler/badge.png?branch=master
    :target: https://coveralls.io/r/semente/django-smuggler?branch=master

**Django Smuggler** is a pluggable application for `Django Web Framework`_ to
easily dump/load fixtures via the automatically-generated administration
interface. A fixture is file with model data serialized to e.g. JSON or XML
that Django knows how to import to the database.

Smuggler is especially useful for transporting database data between production
and development environments, but can also be used as a backup tool.

Project page
    http://github.com/semente/django-smuggler
Translations
    https://www.transifex.com/projects/p/django-smuggler/

.. _`Django Web Framework`: http://www.djangoproject.com


Installing & Setup
==================

Smuggler is in the `Python Package Index (PyPI)`_ and you can easily install
the latest stable version of it using the tools ``pip`` or
``easy_install``. Try::

  pip install django-smuggler

or::

  easy_install django-smuggler

.. _`Python Package Index (PyPI)`: http://pypi.python.org

Alternatively, you can install Smuggler from source code running the follow
command on directory that contains the file ``setup.py``::

  python setup.py install

After installation you need configure your project to recognizes the Smuggler
application adding ``'smuggler'`` to your ``INSTALLED_APPS`` setting and setup
the project *URLConf* like follow::

  urlpatterns = patterns('',
      # ...
      (r'^admin/', include('smuggler.urls')),  # before admin url patterns!
      (r'^admin/', include(admin.site.urls)),
  )

Then try access these urls:

* `/admin/load/ <http://127.0.0.1/admin/load/>`_, to load data from uploaded
  files or files on SMUGGLER_FIXTURE_DIR;

* `/admin/dump/ <http://127.0.0.1/admin/dump/>`_, to download data from
  whole project;

  You can also pass in a querystring like
  ``/admin/dump/?app_label=flatpages,auth,yourapp.model`` to specify what
  must be dumped.

* `/admin/APP_LABEL/dump/ <http://127.0.0.1/admin/APP_LABEL/dump/>`_, to
  download data from a app;

* `/admin/APP_LABEL/MODEL_LABEL/dump/
  <http://127.0.0.1/admin/APP_LABEL/MODEL_LABEL/dump/>`_, to download data
  from a model;

If you can access the URLs above, the application was setup correctly. Note
that these URLs are accessible only by superusers.

Smuggler also provides a template to show buttons for dump and load data on
change list page (``change_list.html``). You can setup the ModelAdmin you are
interested like follow::

    class ExampleAdmin(admin.ModelAdmin):
        change_list_template = 'smuggler/change_list.html'
        ...


Settings
--------

Smuggler has the following settings available. You can set them in your project
``settings.py``. If you doesn't set them it will assume the default values:

SMUGGLER_EXCLUDE_LIST
    List of models to be excluded from dump. Use the form 'app_label.ModelName'.
    Default: [].
                                
SMUGGLER_FIXTURE_DIR
    Uploaded fixtures are stored in this directory (if requested).
    Default: None.

SMUGGLER_FORMAT
    Format for dumped files. Any of the serialization formats supported by
    Django, json, xml and in some cases yaml.
    Default: 'json'.

SMUGGLER_INDENT
    Indentation for dumped files.
    Default: 2.


Screenshots
===========

Buttons on change_list.html:

.. image:: https://github.com/semente/django-smuggler/raw/master/etc/screenshot-0.png
   :alt: buttons on change_list.html
   :align: center

Load form (with ``SMUGGLER_FIXTURE_DIR`` configured):

.. image:: https://github.com/semente/django-smuggler/raw/master/etc/screenshot-1.png
   :alt: load form
   :align: center


Release notes
=============

Version 0.7.0 (2016-02-25)
--------------------------

* Support Django 1.8
* Support Django 1.9
* Drop support for Django < 1.7
* Drop support for Python < 2.7

Version 0.6.1 (2015-11-25)
--------------------------

* Increase Django 1.7 compatibilty by supporting
  use_natural_foreign_keys and use_natural_primary_keys arguments
  for dumpdata

Version 0.6 (2014-09-18)
------------------------

* HTML5 multiple file upload is now supported for fixture uploads

* Support loading fixtures from ``SMUGGLER_FIXTURE_DIR`` and upload at the same time

* Recognize fixtures with upper case file extension correctly

* Loading fixtures now uses loaddata management command

* Removed signals.py

* Removed sample templates

* Cleaner code and better tests :-)


Version 0.5 (2014-08-21)
------------------------

* Added an option to specify a list of app labels to the /dump/ view

* Improved test suite

* Dropped Django 1.3 support

* Preliminary Python 3 support


Version 0.4.1 (2013-11-12)
--------------------------

* Changelist template is now Django 1.6 compatible


Version 0.4 (2013-04-01)
------------------------

* Django 1.5+ support;

* Added German translation;

* Added some tests.


Version 0.3 (2012-01-31)
------------------------

* Significant bug fixes and improvements when loading and exporting data;

* Allow formats for import besides JSON and XML (aa105b3, needs documentation);

* Added Dutch translation.


Version 0.2 (2011-08-19)
------------------------

* Django 1.2+ support;

* Keep uploaded files as alternative choices to import (issues #1 and #6);

* Vulnerability fixed (d73cec6);

* Added Polish, Russian, Catalan and Brazilian Portuguese translations.


Version 0.1.1 (2010-01-20)
--------------------------

* First stable version.


Backwards-incompatible changes
==============================

* Removed AdminFormMixin (Version 0.7)

* Removed signals.py (Version 0.6)

* Renamed urls from import/export to load/dump (Version 0.1)


Contributing
============

If you find any problems in the code or documentation, please take 30 seconds
to fill out a issue `here <https://github.com/semente/django-smuggler/issues>`_.

The contributing with code or translation is MUCH-APPRECIATED. Feel free to
fork or send patchs.

You can translate this application to your language using Transifex. Access
the `project page <https://www.transifex.com/projects/p/django-smuggler/.>`_
on Transifex.

See the AUTHORS file for a complete authors list of this application.

Thanks to `Interaction Consortium <http://interactionconsortium.com/>`_ for
sponsoring the first releases of the project.


Tests
=====

If you are contributing to django-smuggler we recommend setting up a
virtualenv en running::

    pip install -r test-requirements.txt

You can then run the tests with::

    make tests

Before submitting a pull request please test against our supported versions
of Python and Django by running::

    tox

To see if you need to add tests we use coverage. You can generate a coverage
report with::

    make coverage

To check if your code follows the style guide you can run::

   make lint

Copying conditions
==================

Django Smuggler is free software; you can redistribute it and/or modify it
under the terms of the `GNU Lesser General Public License`_ as published by the
Free Software Foundation; either version 3 of the License, or (at your option)
any later version.

Django Smuggler is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this program; see the file COPYING.LESSER. If not, see
http://www.gnu.org/licenses/.

.. _`GNU Lesser General Public License`: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
