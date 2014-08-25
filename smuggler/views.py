# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.
import os.path
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.management.base import CommandError
from django.core.serializers.base import DeserializationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import FormView
from smuggler.forms import ImportForm
from smuggler import settings
from smuggler.utils import (save_uploaded_file_on_disk, serialize_to_response,
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


class LoadDataView(FormView):
    form_class = ImportForm
    template_name = 'smuggler/load_data_form.html'
    success_url = '.'

    def form_valid(self, form):
        uploads = form.cleaned_data.get('uploads', [])
        store = form.cleaned_data.get('store', False)
        picked_files = form.cleaned_data.get('picked_files', [])
        fixtures = []
        for upload in uploads:
            file_name = upload.name
            file_format = os.path.splitext(file_name)[1][1:].lower()
            if store:
                destination_path = os.path.join(
                    settings.SMUGGLER_FIXTURE_DIR, file_name)
                save_uploaded_file_on_disk(upload, destination_path)
                file_data = open(destination_path, 'r')
            elif upload.multiple_chunks():
                file_data = open(upload.temporary_file_path(), 'r')
            else:
                file_data = upload.read()
            fixtures.append((file_format, file_data))
        for file_name in picked_files:
            file_format = os.path.splitext(file_name)[1][1:].lower()
            file_data = open(file_name, 'r')
            fixtures.append((file_format, file_data))
        try:
            obj_count = load_requested_data(fixtures)
            user_msg = ('%(obj_count)d object(s) from %(file_count)d'
                        ' file(s) loaded with success.')  # TODO: pluralize
            user_msg = _(user_msg) % {
                'obj_count': obj_count,
                'file_count': len(fixtures)
            }
            messages.info(self.request, user_msg)
        except (IntegrityError, ObjectDoesNotExist,
                DeserializationError) as e:
            messages.error(
                self.request,
                _('An exception occurred while loading data: %s') % str(e))
        return super(LoadDataView, self).form_valid(form)


load_data = user_passes_test(is_superuser)(LoadDataView.as_view())
