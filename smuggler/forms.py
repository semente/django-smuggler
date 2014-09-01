# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.
import os.path
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.serializers import get_serializer_formats
from django.utils.translation import ugettext_lazy as _
from smuggler import settings


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


class FixturePathField(forms.MultipleChoiceField, forms.FilePathField):
    widget = FilteredSelectMultiple(_('files'), False)

    def __init__(self, path, match=None, **kwargs):
        match = match or (
            '(?i)^.+(%s)$' % '|'.join(
                ['\.%s' % ext for ext in get_serializer_formats()])
        )  # Generate a regex string like: (?i)^.+(\.xml|\.json)$
        super(FixturePathField, self).__init__(path, match=match, **kwargs)
        if not self.required:
            del self.choices[0]  # Remove the empty option


class ImportForm(forms.Form):
    uploads = MultiFixtureField(
        label=_('Upload'),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(ImportForm, self).__init__(*args, **kwargs)
        if settings.SMUGGLER_FIXTURE_DIR:
            self.fields['store'] = forms.BooleanField(
                label=_('Save in fixture directory'),
                required=False,
                help_text=(
                    _('Uploads will be saved to "%(fixture_dir)s".') % {
                        'fixture_dir': settings.SMUGGLER_FIXTURE_DIR
                    })
            )
            self.fields['picked_files'] = FixturePathField(
                settings.SMUGGLER_FIXTURE_DIR,
                label=_('From fixture directory'),
                required=False,
                help_text=(
                    _('Data files from "%(fixture_dir)s".') % {
                        'fixture_dir': settings.SMUGGLER_FIXTURE_DIR
                    })
            )
        else:
            self.fields['uploads'].required = True

    def clean(self):
        super(ImportForm, self).clean()
        if settings.SMUGGLER_FIXTURE_DIR:
            uploads = self.cleaned_data['uploads']
            picked_files = self.cleaned_data['picked_files']
            if not uploads and not picked_files:
                raise forms.ValidationError(
                    _('At least one fixture file needs to be'
                      ' uploaded or selected.'))
        return self.cleaned_data

    class Media:
        css = {
            'all': ['admin/css/forms.css']
        }

        js = [
            'admin/js/core.js',
            'admin/js/jquery.min.js',
            'admin/js/jquery.init.js',
            'admin/js/SelectBox.js',
            'admin/js/SelectFilter2.js'
        ]
