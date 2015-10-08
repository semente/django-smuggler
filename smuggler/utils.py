# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.
import re
from django.core.management import CommandError
from django.core.management.color import no_style
from django.core.management.commands.dumpdata import Command as DumpData
from django.core.management.commands.loaddata import Command as LoadData
from django.db import router
from django.db.utils import DEFAULT_DB_ALIAS
from django.http import HttpResponse
from django.utils.six import StringIO
from smuggler import settings

try:
    allow_migrate = router.allow_migrate
except AttributeError:  # before django 1.7
    allow_migrate = router.allow_syncdb


def save_uploaded_file_on_disk(uploaded_file, destination_path):
    with open(destination_path, 'wb') as fp:
        for chunk in uploaded_file.chunks():
            fp.write(chunk)


def serialize_to_response(app_labels=[], exclude=[], response=None,
                          format=settings.SMUGGLER_FORMAT,
                          indent=settings.SMUGGLER_INDENT):
    response = response or HttpResponse(content_type='text/plain')
    stream = StringIO()
    error_stream = StringIO()
    try:
        dumpdata = DumpData()
        dumpdata.style = no_style()
        dumpdata.execute(*app_labels, **{
            'stdout': stream,
            'stderr': error_stream,
            'exclude': exclude,
            'format': format,
            'indent': indent,
            'use_natural_keys': True,
            'use_natural_foreign_keys': True,
            'use_natural_primary_keys': True
        })
    except SystemExit:
        # Django 1.4's implementation of execute catches CommandErrors and
        # then calls sys.exit(1), we circumvent this here.
        errors = error_stream.getvalue().strip().replace('Error: ', '')
        raise CommandError(errors)
    response.write(stream.getvalue())
    return response


def load_fixtures(fixtures):
    stream = StringIO()
    error_stream = StringIO()
    loaddata = LoadData()
    loaddata.style = no_style()
    loaddata.execute(*fixtures, **{
        'stdout': stream,
        'stderr': error_stream,
        'ignore': True,
        'database': DEFAULT_DB_ALIAS,
        'verbosity': 1
    })
    if hasattr(loaddata, 'loaded_object_count'):
        return loaddata.loaded_object_count
    else:
        # Django < 1.6 has no loaded_object_count attribute, we need
        # to fetch it from stderror :(
        errors = error_stream.getvalue()
        out = stream.getvalue()
        if errors:
            # The only way to handle errors in Django 1.4 is to inspect stdout
            raise CommandError(errors.strip().splitlines()[-1])
        return int(re.search('Installed ([0-9]+)', out.strip()).group(1))
