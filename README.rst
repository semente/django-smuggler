===============
Django Smuggler
===============

**Django Smuggler** is a pluggable application for `Django Web Framework`_ for
you easily import/export fixtures via the automatically-generated
administration interface. Especially useful for transporting data in production
for the development project and vice versa, but can also be used as a backup
tool.

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

* `/admin/import/ <http://127.0.0.1/admin/import/>`_, to upload files to be
  imported;

* `/admin/export/ <http://127.0.0.1/admin/export/>`_, to download data from
  whole project;

* `/admin/APP_LABEL/export/ <http://127.0.0.1/admin/APP_LABEL/export/>`_, to
  download data from a app;

* `/admin/APP_LABEL/MODEL_LABEL/export/
  <http://127.0.0.1/admin/APP_LABEL/MODEL_LABEL/export/>`_, to download data
  from a model;

If you can access the URLs above, the application was setup correctly. Note
that these URLs are accessible only by superusers.

Smuggler also provides a template to show buttons for import and export data on
change list page (``change_list.html``). You can setup the ModelAdmin you are
interested like follow::

    class ExampleAdmin(admin.ModelAdmin):
        change_list_template = 'smuggler/change_list.html'
        ...

*Note: on directory "etc/sample_templates/" you have some template examples
to put Smuggler's buttons on app indexes and admin index page.*

Settings
````````

Smuggler has the following settings available. You can set them in your project
``settings.py``. If you doesn't set them it will assume the default values:

SMUGGLER_EXCLUDE_LIST
    List of models to be excluded from exportation. Use the form
    'app_label.ModelName'.
    Default: [].
                                
SMUGGLER_FIXTURE_DIR
    To be used with signal ``smuggler.signals.save_data_on_filesystem``.
    Default: None.

SMUGGLER_FORMAT
    Format for exported files. 'json' and 'xml' are supported.
    Default: 'json'.

SMUGGLER_INDENT
    Indentation for exported files.
    Default: 4.


Screenshots
===========

Import form:

.. image:: http://github.com/semente/django-smuggler/raw/master/etc/screenshot-0.png
   :alt: buttons on change_list.html
   :align: center

Buttons on change_list.html:

.. image:: http://github.com/semente/django-smuggler/raw/master/etc/screenshot-1.png
   :alt: import form
   :align: center


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
