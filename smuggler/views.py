# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

import os
from datetime import datetime
from django.core import serializers
from django.db.models import get_app, get_apps, get_model, get_models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from smuggler.forms import ImportFileForm
from smuggler.settings import SMUGGLER_FORMAT, SMUGGLER_FIXTURE_DIR
from smuggler.utils import (get_excluded_models_set, get_file_list,
                            save_uploaded_file_on_disk, serialize_to_response,
                            superuser_required)

def dump_data(request):
    """Exports data from whole project.
    """
    objects = []
    for app in get_apps():
        models = set(get_models(app)) - get_excluded_models_set()
        for model in models:
            if not model._meta.proxy:
                objects.extend(model._default_manager.all())
    filename = '%s.%s' % (datetime.now().isoformat(), SMUGGLER_FORMAT)
    response = HttpResponse(mimetype="text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return serialize_to_response(objects, response)
dump_data = superuser_required(dump_data)

def dump_app_data(request, app_label):
    """Exports data from a application.
    """
    objects = []
    models = set(get_models(get_app(app_label))) - get_excluded_models_set()
    for model in models:
        if not model._meta.proxy:
            objects.extend(model._default_manager.all())
    filename = '%s_%s.%s' % (app_label, datetime.now().isoformat(),
                             SMUGGLER_FORMAT)
    response = HttpResponse(mimetype="text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return serialize_to_response(objects, response)
dump_app_data = superuser_required(dump_app_data)

def dump_model_data(request, app_label, model_label):
    """Exports data from a model.
    """
    model = get_model(app_label, model_label)
    objects = model._default_manager.all()
    filename = '%s-%s_%s.%s' % (app_label, model_label,
                                datetime.now().isoformat(), SMUGGLER_FORMAT)
    response = HttpResponse(mimetype="text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return serialize_to_response(objects, response)
dump_model_data = superuser_required(dump_model_data)

def load_data(request):
    """
    Load data from uploaded file or disk.

    Note: A uploaded file will be saved on `SMUGGLER_FIXTURE_DIR` if the submit
          button with name "_loadandsave" was pressed.
    """
    form = ImportFileForm()
    if request.method == 'POST':
        data = []
        if request.POST.has_key('_load') or request.POST.has_key('_loadandsave'):
            form = ImportFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = request.FILES['file']
                file_name = uploaded_file.name
                file_format = file_name.split('.')[-1]
                if request.POST.has_key('_loadandsave'):
                    destination_path = os.path.join(SMUGGLER_FIXTURE_DIR,
                                                    file_name)
                    save_uploaded_file_on_disk(uploaded_file, destination_path)
                    file_data = open(destination_path, 'r')
                elif uploaded_file.multiple_chunks():
                    file_data = open(uploaded_file.temporary_file_path(), 'r')
                else:
                    file_data = uploaded_file.read()
                data.append((file_format, file_data))
        elif request.POST.has_key('_loadfromdisk'):
            query_dict = request.POST.copy()        
            del(query_dict['_loadfromdisk'])
            del(query_dict['csrfmiddlewaretoken'])
            selected_files = query_dict.values()
            for file_name in selected_files:
                file_path = os.path.join(SMUGGLER_FIXTURE_DIR, file_name)
                file_format = file_name.split('.')[-1]
                file_data = open(file_path, 'r')
                data.append((file_format, file_data))
        counter = 0
        for format, stream in data:
            objects = serializers.deserialize(format, stream)
            for obj in objects:
                counter += 1
                obj.save()
        if data:
            user_msg = ('%(obj_count)d object(s) from %(file_count)d file(s) '
                        'loaded with success.') # TODO: pluralize
            user_msg = _(user_msg) % {
                'obj_count': counter,
                'file_count': len(data)
            }
            request.user.message_set.create(message=user_msg)
    context = {
        'files_available': get_file_list(SMUGGLER_FIXTURE_DIR) \
            if SMUGGLER_FIXTURE_DIR else [],
        'smuggler_fixture_dir': SMUGGLER_FIXTURE_DIR,
        'import_file_form': form,
    }
    return render_to_response('smuggler/load_data_form.html', context,
                              context_instance=RequestContext(request))
load_data = superuser_required(load_data)
