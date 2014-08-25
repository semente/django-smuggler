# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.core.management import CommandError
from django.core.management.color import no_style
from django.core.management.commands.dumpdata import Command as DumpData
from django.core.management.commands.loaddata import Command as LoadData
from django.db import router
from django.db.utils import DEFAULT_DB_ALIAS
from django.http import HttpResponse
from django.utils.six import StringIO
from smuggler.settings import (SMUGGLER_FORMAT, SMUGGLER_INDENT)

try:
    allow_migrate = router.allow_migrate
except AttributeError:  # before django 1.7
    allow_migrate = router.allow_syncdb


def save_uploaded_file_on_disk(uploaded_file, destination_path):
    with open(destination_path, 'wb') as fp:
        for chunk in uploaded_file.chunks():
            fp.write(chunk)


def serialize_to_response(app_labels=[], exclude=[], response=None,
                          format=SMUGGLER_FORMAT, indent=SMUGGLER_INDENT):
    response = response or HttpResponse(content_type='text/plain')
    stream = StringIO()
    error_stream = StringIO()
    try:
        dumpdata = DumpData()
        dumpdata.style = no_style()
        dumpdata.execute(*app_labels, **{
            'exclude': exclude,
            'format': format,
            'indent': indent,
            'show_traceback': True,
            'use_natural_keys': True,
            'stdout': stream,
            'stderr': error_stream
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
    try:
        loaddata = LoadData()
        loaddata.style = no_style()
        loaddata.execute(*fixtures, **{
            'stdout': stream,
            'stderr': error_stream,
            'ignore': True,
            'database': DEFAULT_DB_ALIAS,
            'verbosity': 0
        })
        return loaddata.loaded_object_count
    except SystemExit:
        # Django 1.4's implementation of execute catches CommandErrors and
        # then calls sys.exit(1), we circumvent this here.
        errors = error_stream.getvalue().strip().replace('Error: ', '')
        raise CommandError(errors)
