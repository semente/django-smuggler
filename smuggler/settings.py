# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.conf import settings

SMUGGLER_EXCLUDE_LIST = getattr(settings, 'SMUGGLER_EXCLUDE_LIST', [])
SMUGGLER_FIXTURE_DIR = getattr(settings, 'SMUGGLER_FIXTURE_DIR', None)
SMUGGLER_FORMAT = getattr(settings, 'SMUGGLER_FORMAT', 'json')
SMUGGLER_INDENT = getattr(settings, 'SMUGGLER_INDENT', 2)
