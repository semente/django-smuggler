# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.
import os.path
from django import forms
from django.core.serializers import get_serializer_formats
from django.utils.translation import ugettext_lazy as _


class MultiFileInput(forms.FileInput):
    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['multiple'] = 'multiple'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        if name in files:
            return [files.get(name)]
        return []


class MultiFixtureField(forms.FileField):
    widget = MultiFileInput

    def to_python(self, data):
        files = []
        for item in data:
            files.append(super(MultiFixtureField, self).to_python(item))
        return files

    def validate(self, data):
        super(MultiFixtureField, self).validate(data)
        for upload in data:
            file_format = os.path.splitext(upload.name)[1][1:].lower()
            if file_format not in get_serializer_formats():
                raise forms.ValidationError(
                    _('Invalid file extension: .%(extension)s.') % {
                        'extension': file_format
                    })
        return data


class ImportForm(forms.Form):
    uploads = MultiFixtureField(
        label=_('Fixture(s) to load'),
        help_text=_('Existing items with same <em>primary key</em>'
                    ' will be overwritten.'),
        required=True
    )

    class Media:
        css = {
            'all': ['admin/css/forms.css']
        }
