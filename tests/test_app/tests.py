import re
import StringIO

from django.contrib.flatpages.models import FlatPage
from django.core.management import CommandError
from django.test import TestCase
from unittest2 import TestCase as TestCase2
from smuggler import utils


class BasicDumpTestCase(TestCase, TestCase2):
    SITE_DUMP = '{ "pk": 1, "model": "sites.site", "fields": { "domain": "example.com", "name": "example.com" } }'
    FLATPAGE_DUMP = '{ "pk": 1, "model": "flatpages.flatpage", "fields": { "registration_required": false, "title": "test", "url": "/", "template_name": "", "sites": [], "content": "", "enable_comments": false } }'
    BASIC_DUMP = '[ %s, %s ]' % (SITE_DUMP, FLATPAGE_DUMP)

    def setUp(self):
        f = FlatPage(url='/', title='test')
        f.save()

    def normalize(self, out):
        return re.sub(r'\s\s*', ' ', out).strip()

    def test_serialize_to_response(self):
        stream = StringIO.StringIO()
        utils.serialize_to_response(response=stream)
        out = self.normalize(stream.getvalue())
        self.assertEquals(out, self.BASIC_DUMP)

    def test_serialize_exclude(self):
        stream = StringIO.StringIO()
        utils.serialize_to_response(exclude=['sites'], response=stream)
        out = self.normalize(stream.getvalue())
        self.assertEquals(out, '[ %s ]' % self.FLATPAGE_DUMP)

    def test_serialize_include(self):
        stream = StringIO.StringIO()
        utils.serialize_to_response(app_labels=['sites'], response=stream)
        out = self.normalize(stream.getvalue())
        self.assertEquals(out, '[ %s ]' % self.SITE_DUMP)

    def test_serialize_unknown_app_fail(self):
        self.assertRaises(CommandError, utils.serialize_to_response, 'auth')
