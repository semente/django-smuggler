# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.conf.urls import url, include

from smuggler.views import dump_app_data, dump_data, dump_model_data, load_data


urlpatterns = [
    url(r'^dump/$', dump_data, name='dump-data'),
    url(r'^(?P<app_label>\w+)/', include([
        url(r'^dump/$', dump_app_data, name='dump-app-data'),
        url(r'^(?P<model_label>\w+)/dump/$', dump_model_data,
            name='dump-model-data'),
    ])),
    url(r'^load/$', load_data, name='load-data')
]
