# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.management.base import CommandError
from django.core.serializers.base import DeserializationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from smuggler.forms import ImportFileForm
from smuggler import settings
from smuggler.utils import (get_file_list,
                            save_uploaded_file_on_disk, serialize_to_response,
                            load_requested_data)


def dump_to_response(request, app_label=[], exclude=[], filename_prefix=None):
    """Utility function that dumps the given app/model to an HttpResponse.
    """
    try:
        filename = '%s.%s' % (datetime.now().isoformat(),
                              settings.SMUGGLER_FORMAT)
        if filename_prefix:
            filename = '%s_%s' % (filename_prefix, filename)
        if not isinstance(app_label, list):
            app_label = [app_label]
        response = serialize_to_response(app_label, exclude)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    except CommandError as e:
        messages.error(
            request,
            _('An exception occurred while dumping data: %s') % force_text(e))
    return HttpResponseRedirect(request.build_absolute_uri().split('dump')[0])


def is_superuser(u):
    if u.is_authenticated():
        if u.is_superuser:
            return True
        raise PermissionDenied
    return False


@user_passes_test(is_superuser)
def dump_data(request):
    """Exports data from whole project.
    """
    # Try to grab app_label data
    app_label = request.GET.get('app_label', [])
    if app_label:
        app_label = app_label.split(',')
    return dump_to_response(request, app_label=app_label,
                            exclude=settings.SMUGGLER_EXCLUDE_LIST)


@user_passes_test(is_superuser)
def dump_app_data(request, app_label):
    """Exports data from a application.
    """
    return dump_to_response(request, app_label, settings.SMUGGLER_EXCLUDE_LIST,
                            app_label)


@user_passes_test(is_superuser)
def dump_model_data(request, app_label, model_label):
    """Exports data from a model.
    """
    return dump_to_response(request, '%s.%s' % (app_label, model_label),
                            [], '-'.join((app_label, model_label)))


@user_passes_test(is_superuser)
def load_data(request):
    """
    Load data from uploaded file or disk.

    Note: A uploaded file will be saved on `SMUGGLER_FIXTURE_DIR` if the submit
          button with name "_loadandsave" was pressed.
    """
    form = ImportFileForm()
    if request.method == 'POST':
        data = []
        if '_load' in request.POST or '_loadandsave' in request.POST:
            form = ImportFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = request.FILES['file']
                file_name = uploaded_file.name
                file_format = file_name.split('.')[-1]
                if '_loadandsave' in request.POST:
                    destination_path = os.path.join(
                        settings.SMUGGLER_FIXTURE_DIR, file_name)
                    save_uploaded_file_on_disk(uploaded_file, destination_path)
                    file_data = open(destination_path, 'r')
                elif uploaded_file.multiple_chunks():
                    file_data = open(uploaded_file.temporary_file_path(), 'r')
                else:
                    file_data = uploaded_file.read()
                data.append((file_format, file_data))
        elif '_loadfromdisk' in request.POST:
            query_dict = request.POST.copy()
            del(query_dict['_loadfromdisk'])
            del(query_dict['csrfmiddlewaretoken'])
            selected_files = query_dict.values()
            for file_name in selected_files:
                file_path = os.path.join(
                    settings.SMUGGLER_FIXTURE_DIR, file_name)
                file_format = file_name.split('.')[-1]
                file_data = open(file_path, 'r')
                data.append((file_format, file_data))
        if data:
            try:
                obj_count = load_requested_data(data)
                user_msg = ('%(obj_count)d object(s) from %(file_count)d'
                            ' file(s) loaded with success.')  # TODO: pluralize
                user_msg = _(user_msg) % {
                    'obj_count': obj_count,
                    'file_count': len(data)
                }
                messages.add_message(request, messages.INFO, user_msg)
            except (IntegrityError, ObjectDoesNotExist,
                    DeserializationError) as e:
                messages.add_message(
                    request, messages.ERROR,
                    _(u'An exception occurred while loading data: %s')
                    % str(e))
    context = {
        'files_available': (get_file_list(settings.SMUGGLER_FIXTURE_DIR)
                            if settings.SMUGGLER_FIXTURE_DIR else []),
        'smuggler_fixture_dir': settings.SMUGGLER_FIXTURE_DIR,
        'import_file_form': form,
    }
    return TemplateResponse(request, 'smuggler/load_data_form.html', context)
