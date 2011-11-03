# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers import get_serializer_formats
from django.utils.translation import ugettext as _

class ImportFileForm(forms.Form):
    file = forms.FileField(
        label='File to load',
        help_text=_('Existing items with same <i>id</i> will be overwritten.'),
        required=True,
    )

    def clean_file(self):
        data = self.cleaned_data['file']
        if not isinstance(data, InMemoryUploadedFile):
            return data
        file_format = data.name.split('.')[-1]
        if not file_format in get_serializer_formats():
            raise forms.ValidationError(_('Invalid file extension.'))
        return data
