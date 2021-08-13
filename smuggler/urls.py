# Copyright (c) 2009 Guilherme Semente and contributors
#
# This file is part of Django Smuggler.
#
# Django Smuggler is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.urls import include, path

from smuggler.views import dump_app_data, dump_data, dump_model_data, load_data

urlpatterns = [
    path("dump/", dump_data, name="dump-data"),
    path(
        "<slug:app_label>/",
        include(
            [
                path("dump/", dump_app_data, name="dump-app-data"),
                path(
                    "<slug:model_label>/dump/", dump_model_data, name="dump-model-data"
                ),
            ]
        ),
    ),
    path("load/", load_data, name="load-data"),
]
