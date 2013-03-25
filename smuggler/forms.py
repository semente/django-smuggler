# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.
import django
from django.conf import settings
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers import get_serializer_formats
from django.utils.translation import ugettext as _

if django.VERSION > (1, 3):
    ADMIN_MEDIA_PREFIX = 'admin/'
else:
    ADMIN_MEDIA_PREFIX = settings.ADMIN_MEDIA_PREFIX


class ImportFileForm(forms.Form):
    file = forms.FileField(
        label='File to load',
        help_text=_('Existing items with same <i>id</i> will be overwritten.'),
        required=True,
    )

    class Media:
        css = {
            'all': [''.join((ADMIN_MEDIA_PREFIX, 'css/forms.css'))]
        }

    def clean_file(self):
        data = self.cleaned_data['file']
        if not isinstance(data, InMemoryUploadedFile):
            return data
        file_format = data.name.split('.')[-1]
        if not file_format in get_serializer_formats():
            raise forms.ValidationError(_('Invalid file extension.'))
        return data
