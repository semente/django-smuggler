# Copyright (c) 2009 Guilherme Semente and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.
import re

from io import StringIO

from django.core.management import call_command
from django.db.utils import DEFAULT_DB_ALIAS
from django.http import HttpResponse

from smuggler import settings


def save_uploaded_file_on_disk(uploaded_file, destination_path):
    with open(destination_path, "wb") as fp:
        for chunk in uploaded_file.chunks():
            fp.write(chunk)


def serialize_to_response(
    app_labels=None,
    exclude=None,
    response=None,
    format=settings.SMUGGLER_FORMAT,
    indent=settings.SMUGGLER_INDENT,
):
    app_labels = app_labels or []
    exclude = exclude or []
    response = response or HttpResponse(content_type="text/plain")
    stream = StringIO()
    error_stream = StringIO()
    call_command(
        "dumpdata",
        *app_labels,
        **{
            "stdout": stream,
            "stderr": error_stream,
            "exclude": exclude,
            "format": format,
            "indent": indent,
            "use_natural_foreign_keys": True,
            "use_natural_primary_keys": True,
        }
    )
    response.write(stream.getvalue())
    return response


def load_fixtures(fixtures):
    stream = StringIO()
    error_stream = StringIO()
    call_command(
        "loaddata",
        *fixtures,
        **{
            "stdout": stream,
            "stderr": error_stream,
            "ignore": True,
            "database": DEFAULT_DB_ALIAS,
            "verbosity": 1,
        }
    )
    stream.seek(0)
    result = stream.read()
    return int(re.match(r"Installed\s([0-9]+)\s.*", result).groups()[0])
