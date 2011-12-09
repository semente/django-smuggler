# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.
import os
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.management.color import no_style
from django.db import connections, router, transaction
from django.db.models import get_model
from django.db.utils import DEFAULT_DB_ALIAS
from django.http import HttpResponse
from smuggler.settings import (SMUGGLER_EXCLUDE_LIST, SMUGGLER_FORMAT,
                               SMUGGLER_INDENT)

def get_excluded_models_set():
    excluded_models = set([])
    for label in SMUGGLER_EXCLUDE_LIST:
        app_label, model_label = label.split('.')
        excluded_models.add(get_model(app_label, model_label))
    return excluded_models

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

def serialize_to_response(queryset, response=HttpResponse(),
                          format=SMUGGLER_FORMAT, indent=SMUGGLER_INDENT):
    serializers.serialize(format, queryset, indent=indent, stream=response)
    return response

def load_requested_data(data):
    """
    Load the given data dumps and return the number of imported objects.

    Wraps the entire action in a big transaction.
    """
    style = no_style()

    using = DEFAULT_DB_ALIAS
    connection = connections[using]
    cursor = connection.cursor()

    transaction.commit_unless_managed(using=using)
    transaction.enter_transaction_management(using=using)
    transaction.managed(True, using=using)
    
    models = set()
    counter = 0
    try:
        for format, stream in data:
            objects = serializers.deserialize(format, stream)
            for obj in objects:
                model = obj.object.__class__
                if router.allow_syncdb(using, model):
                    models.add(model)
                    counter += 1
                    obj.save(using=using)
        if counter > 0:
            sequence_sql = connection.ops.sequence_reset_sql(style, models)
            if sequence_sql:
                for line in sequence_sql:
                    cursor.execute(line)
    except Exception, e:
        transaction.rollback(using=using)
        transaction.leave_transaction_management(using=using)
        raise e
    transaction.commit(using=using)
    transaction.leave_transaction_management(using=using)
    connection.close()
    return counter

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
