#/usr/bin/env python
#
# Copyright (c) 2009-2013 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

import codecs
import os
import sys

from setuptools import setup, find_packages


if 'publish' in sys.argv:
    os.system('python setup.py sdist upload')
    sys.exit()

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


# Dynamically calculate the version based on smuggler.VERSION.
version = __import__('smuggler').get_version()

setup(
    name='django-smuggler',
    version=version,
    description=('Pluggable application for Django that helps you to '
                 'import/export fixtures via the administration interface'),
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    keywords='django apps tools backup fixtures admin',
    author='Guilherme Gondim',
    author_email='semente+django-smuggler@taurinus.org',
    maintainer='Guilherme Gondim',
    maintainer_email='semente+django-smuggler@taurinus.org',
    license='GNU Lesser General Public License v3 or later (LGPLv3+)',
    url='http://github.com/semente/django-smuggler',
    download_url='http://github.com/semente/django-smuggler/downloads',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=['unittest2'],
)
