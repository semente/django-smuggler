===============
Django Smuggler
===============

**Django Smuggler** is a pluggable application for `Django Web Framework`_ for
you easily dump/load fixtures via the automatically-generated administration
interface. Especially useful for transporting data in production for the
development project and vice versa, but can also be used as a backup tool.

Project page
    http://github.com/semente/django-smuggler
Translations
    https://www.transifex.net/projects/p/django-smuggler/

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
      (r'^admin/', include('smuggler.urls')), # put it before admin url patterns
      (r'^admin/', include(admin.site.urls)),
  )

Then try access these urls:

* `/admin/load/ <http://127.0.0.1/admin/load/>`_, to load data from uploaded
  files or files on SMUGGLER_FIXTURE_DIR;

* `/admin/dump/ <http://127.0.0.1/admin/dump/>`_, to download data from
  whole project;

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

*Note: on directory "etc/sample_templates/" you have some template examples
to put Smuggler's buttons on app indexes and admin index page.*

Settings
--------

Smuggler has the following settings available. You can set them in your project
``settings.py``. If you doesn't set them it will assume the default values:

SMUGGLER_EXCLUDE_LIST
    List of models to be excluded from dump. Use the form 'app_label.ModelName'.
    Default: [].
                                
SMUGGLER_FIXTURE_DIR
    Saved files will be stored on this directory. The signal
    ``smuggler.signals.save_data_on_filesystem`` uses this value too.
    Default: None.

SMUGGLER_FORMAT
    Format for dumped files. 'json' and 'xml' are supported.
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

Load form:

.. image:: https://github.com/semente/django-smuggler/raw/master/etc/screenshot-1.png
   :alt: load form
   :align: center



Backwards-incompatible changes
==============================

Since version 0.1
-----------------

2010-02-11
    Renamed urls from import/export to load/dump to reflect recent
    changes (c276b07)


Contributing
============

If you find any problems in the code or documentation, please take 30 seconds
to fill out a issue `here <http://github.com/semente/django-smuggler/issues>`_.

The contributing with code or translation is MUCH-APPRECIATED. Feel free to
fork or send patchs.

You can translate this application to your language using Transifex. Access
the `project page <https://www.transifex.net/projects/p/django-smuggler/.>`_
on Transifex.

See the AUTHORS file for a complete authors list of this application.

Thanks to `Interaction Consortium <http://interactionconsortium.com/>`_ for
sponsoring the first releases of the project.


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
