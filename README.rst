===============
Django Smuggler
===============

**Django Smuggler** is a pluggable application for `Django Web Framework`_ that
help you import/export fixtures via the automatically-generated admin
interface.

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

Finally, setup the ModelAdmin you are interested to show Smuggler's options on
change list page::

    class ExampleAdmin(admin.ModelAdmin):
        change_list_template = 'smuggler/change_list.html'
        ...


Copying conditions
==================

Django Smuggler is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation; either version 3 of the License, or (at
your option) any later version.

Django Smuggler is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; see the file COPYING.LESSER. If not, see
<http://www.gnu.org/licenses/>.
