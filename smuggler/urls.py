# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.conf.urls.defaults import *
from smuggler.views import (dump_data, dump_app_data, dump_model_data,
                            load_data)

dump_data_url = url(
    regex=r'^dump/$',
    view=dump_data,
    name='dump-data'
)

dump_app_data_url = url(
    regex=r'^(?P<app_label>\w+)/dump/$',
    view=dump_app_data,
    name='dump-app-data'
)

dump_model_data_url = url(
    regex=r'^(?P<app_label>\w+)/(?P<model_label>\w+)/dump/$',
    view=dump_model_data,
    name='dump-model-data'
)

load_data_url = url(
    regex=r'^load/$',
    view=load_data,
    name='load-data'
)

urlpatterns = patterns('', dump_model_data_url, dump_app_data_url,
                       dump_data_url, load_data_url)
