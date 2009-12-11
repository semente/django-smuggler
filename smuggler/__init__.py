# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

VERSION = (0, 1, 'pre')

def get_version():
    """
    Returns the version as a human-format string.
    """
    v = '.'.join([str(i) for i in VERSION[:-1]])
    return '%s-%s' % (v, VERSION[-1])

__author__ = 'See the file AUTHORS.'
__license__ = 'GNU Lesser General Public License (GPL), Version 3'
__url__ = 'http://github.com/semente/django-smuggler'
__version__ = get_version()
