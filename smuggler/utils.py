# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

import os
from django.core.exceptions import PermissionDenied
from django.core.management.commands.dumpdata import Command as DumpData
from django.http import HttpResponse
from smuggler.settings import (SMUGGLER_FORMAT, SMUGGLER_INDENT)

def get_file_list(path):
    file_list = []
    for file_name in os.listdir(path):
        if not os.path.isdir(file_name):
            file_path = os.path.join(path, file_name)
            file_size = os.path.getsize(file_path)
            file_list.append((file_name, '%0.1f KB'%float(file_size/1024.0)))
    file_list.sort()
    return file_list

def save_uploaded_file_on_disk(uploaded_file, destination_path):
    destination = open(destination_path, 'w')
    for chunk in uploaded_file.chunks():
        destination.write(chunk)
    destination.close()

def serialize_to_response(app_labels=[], exclude=[], response=None,
                          format=SMUGGLER_FORMAT, indent=SMUGGLER_INDENT):
    response = response or HttpResponse(mimetype='text/plain')
    response.write(DumpData().handle(*app_labels, **{
        'exclude': exclude,
        'format': format,
        'indent': indent,
        'show_traceback': True,
        'use_natural_keys': True
    }))
    return response

def superuser_required(function):
    """
    Decorator for views that checks if the logged user is a superuser. In other
    words, deny access from non-superusers.
    """
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner
