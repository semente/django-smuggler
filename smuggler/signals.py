# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from smuggler.settings import SMUGGLER_FIXTURE_DIR, SMUGGLER_FORMAT

def save_data_on_filesystem(sender, **kwargs):
    if not SMUGGLER_FIXTURE_DIR:
        # TODO: improve exception
        raise ImproperlyConfigured
    objects = sender._default_manager.all()
    app_label, model_label = sender._meta.app_label, sender._meta.module_name
    filename = '%s-%s.%s' % (app_label, model_label, SMUGGLER_FORMAT)
    fixture = file(SMUGGLER_FIXTURE_DIR + '/' + filename, 'w')
    serializers.serialize(SMUGGLER_FORMAT, objects, indent=indent, stream=fixture)
    fixture.close()
