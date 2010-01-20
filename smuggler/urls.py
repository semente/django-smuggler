# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.conf.urls.defaults import *
from smuggler.views import export_data, import_data

export_data_url = url(
    regex=r'^(?P<app_label>\w+)/(?P<model_label>\w+)/export/$',
    view=export_data,
    name='export-data'
)

import_data_url = url(
    regex=r'^import/$',
    view=import_data,
    name='import-data',
)

urlpatterns = patterns('', export_data_url, import_data_url)
