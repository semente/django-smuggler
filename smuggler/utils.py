# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.core import serializers
from django.http import HttpResponse
from smuggler.settings import SMUGGLER_FORMAT, SMUGGLER_INDENT

def serialize_to_response(queryset, response=HttpResponse(),
                          format=SMUGGLER_FORMAT, indent=SMUGGLER_INDENT):
    serializers.serialize(format, queryset, indent=indent, stream=response)
    return response
