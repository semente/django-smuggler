# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

"""
Django Smuggler is a pluggable application for Django Web Framework that help
you dump/load fixtures via the automatically-generated admin interface.
"""

VERSION = (0, 8, 0)


def get_version():
    """
    Returns the version as a human-format string.
    """
    return '.'.join([str(i) for i in VERSION])

__author__ = 'See the file AUTHORS.'
__license__ = 'GNU Lesser General Public License v3 or later (LGPLv3+)'
__url__ = 'https://github.com/semente/django-smuggler'
__version__ = get_version()
