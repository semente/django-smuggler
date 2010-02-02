# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from datetime import datetime
from django.core import serializers
from django.db.models import get_app, get_apps, get_model, get_models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from smuggler.forms import ImportDataForm
from smuggler.settings import SMUGGLER_FORMAT
from smuggler.utils import (get_excluded_models_set, serialize_to_response,
                            superuser_required)

def export_data(request):
    """Exports data from whole project.
    """
    objects = []
    for app in get_apps():
        for model in set(get_models(app)) - get_excluded_models_set():
            if not model._meta.proxy:
                objects.extend(model._default_manager.all())
    filename = '%s.%s' % (datetime.now().isoformat(), SMUGGLER_FORMAT)
    response = HttpResponse(mimetype="text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return serialize_to_response(objects, response)
export_data = superuser_required(export_data)

def export_app_data(request, app_label):
    """Exports data from a application.
    """
    objects = []
    for model in set(get_models(get_app(app_label))) - get_excluded_models_set():
        if not model._meta.proxy:
            objects.extend(model._default_manager.all())
    filename = '%s_%s.%s' % (app_label, datetime.now().isoformat(),
                             SMUGGLER_FORMAT)
    response = HttpResponse(mimetype="text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return serialize_to_response(objects, response)
export_app_data = superuser_required(export_app_data)

def export_model_data(request, app_label, model_label):
    """Exports data from a model.
    """
    model = get_model(app_label, model_label)
    objects = model._default_manager.all()
    filename = '%s-%s_%s.%s' % (app_label, model_label,
                                datetime.now().isoformat(), SMUGGLER_FORMAT)
    response = HttpResponse(mimetype="text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return serialize_to_response(objects, response)
export_model_data = superuser_required(export_model_data)

def import_data(request):
    """Import data from uploaded file.
    """
    if request.method == 'POST':
        form = ImportDataForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            if uploaded_file.multiple_chunks():
                data = file(uploaded_file.temporary_file_path(), 'r')
            else:
                data = uploaded_file.read()
            if uploaded_file.content_type == 'text/xml':
                file_ext = 'xml'
            elif uploaded_file.content_type == 'application/json':
                file_ext = 'json'
            else:
                # Fallback to "json" because on some tests the ``content_type``
                # of JSON files was "application/octet-stream".
                file_ext = 'json'
            objects = serializers.deserialize(file_ext, data)
            for obj in objects:
                obj.save()
            user_msg = _('Data imported with success.')
            request.user.message_set.create(message=user_msg)
            return HttpResponseRedirect('./')
    else:
        form = ImportDataForm()
    context = {'form': form}
    return render_to_response(
        'smuggler/import_data_form.html',
        context,
        context_instance=RequestContext(request)
    )
import_data = superuser_required(import_data)
