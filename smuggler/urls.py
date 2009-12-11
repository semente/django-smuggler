# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.conf.urls.defaults import *

urlpatterns = patterns('smuggler.views',
    (r'^(?P<app_label>\w+)/(?P<model_label>\w+)/export/$', 'export_data'),
    (r'^(?P<app_label>\w+)/(?P<model_label>\w+)/import/$', 'import_data'),
)
