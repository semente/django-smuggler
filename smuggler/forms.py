# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django import forms
from django.utils.translation import ugettext as _

class ImportDataForm(forms.Form):
    file = forms.FileField(
        label="File",
        help_text=_("Fixture file to import. <b>Note: existing items with same "
                    "<i>id</i>, will be overwrited.</b>"),
        required=True
    )
