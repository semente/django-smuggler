#!/usr/bin/env python
import django
from django.core import management
import os.path
import sys

path, scriptname = os.path.split(__file__)

sys.path.append(os.path.abspath(path))
sys.path.append(os.path.abspath(os.path.join(path, '..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'

if django.VERSION[0:2] >= (1, 7):
    django.setup()

management.call_command('test', 'test_app')
