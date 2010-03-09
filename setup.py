# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from smuggler import get_version

setup(
    name = 'django-smuggler',
    version = get_version(),
    description = 'dump/load fixtures via Django admin interface',
    long_description = ('Django Smuggler is a pluggable application for Django '
                        'Web Framework for you easily dump/load fixtures '
                        'via the automatically-generated administration '
                        'interface. Especially useful for transporting data in '
                        'production for the development project and vice'
                        'versa, but can also be used as a backup tool.'),
    keywords = 'django apps tools backup fixtures admin',
    author = 'Guilherme Gondim',
    author_email = 'semente@taurinus.org',
    url = 'http://github.com/semente/django-smuggler',
    download_url = 'http://github.com/semente/django-smuggler/downloads',
    license = 'GNU Lesser General Public License (LGPL), Version 3',
    classifiers = [
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
)
