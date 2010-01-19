# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from datetime import datetime
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from smuggler.settings import (SMUGGLER_FIXTURE_DIR, SMUGGLER_FORMAT,
                               SMUGGLER_INDENT)

def save_data_on_filesystem(sender, **kwargs):
    if not SMUGGLER_FIXTURE_DIR:
        raise ImproperlyConfigured('You need to specify SMUGGLER_FIXTURE_DIR in '
                                   'your Django settings file.')
    objects = sender._default_manager.all()
    app_label, model_label = sender._meta.app_label, sender._meta.module_name
    filename = '%s-%s_%s.%s' % (app_label, model_label,
                                datetime.now().isoformat(), SMUGGLER_FORMAT)
    fixture = file(SMUGGLER_FIXTURE_DIR + '/' + filename, 'w')
    serializers.serialize(SMUGGLER_FORMAT, objects, indent=SMUGGLER_INDENT,
                          stream=fixture)
    fixture.close()
