# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from smuggler.settings import SMUGGLER_FORMAT, SMUGGLER_INDENT

def serialize_to_response(queryset, response=HttpResponse(),
                          format=SMUGGLER_FORMAT, indent=SMUGGLER_INDENT):
    serializers.serialize(format, queryset, indent=indent, stream=response)
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
