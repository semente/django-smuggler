# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.conf.urls import url


urlpatterns = [
    url(r'^dump/$',
        'smuggler.views.dump_data',
        name='dump-data'),
    url(r'^(?P<app_label>\w+)/dump/$',
        'smuggler.views.dump_app_data',
        name='dump-app-data'),
    url(r'^(?P<app_label>\w+)/(?P<model_label>\w+)/dump/$',
        'smuggler.views.dump_model_data',
        name='dump-model-data'),
    url(r'^load/$',
        'smuggler.views.load_data',
        name='load-data')
]
