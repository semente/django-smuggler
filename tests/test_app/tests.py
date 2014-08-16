import json
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

    def dictsMatch(self, d1, d2, parent=''):
        if len(d1.keys()) != len(d1.keys()):
            return False
        d1keys = d1.keys()
        d1keys.sort()
        d2keys = d2.keys()
        d2keys.sort()
        for k1, k2 in zip(d1keys, d2keys):
            if k1 != k2:
                return False
            else:
                if type(d1[k1])==type({}):
                    if not self.dictsMatch(d1[k1], d2[k1], k1):
                        return False
                else:
                    if d1[k1]!=d2[k1]:
                        return False
        return True

    def assertDictsMatch(self, d1, d2):
        try:
            self.assertTrue(self.dictsMatch(
                d1, d2))
        except AssertionError: 
            self.assertEquals(d1, d2)

    def test_serialize_to_response(self):
        stream = StringIO.StringIO()
        utils.serialize_to_response(response=stream)
        out = self.normalize(stream.getvalue())
        basic_out = json.loads(out)

        self.assertDictsMatch(
            basic_out[0],
            json.loads(self.SITE_DUMP),
        )
        self.assertDictsMatch(
            basic_out[1],
            json.loads(self.FLATPAGE_DUMP),
        )

    def test_serialize_exclude(self):
        stream = StringIO.StringIO()
        utils.serialize_to_response(exclude=['sites'], response=stream)
        out = self.normalize(stream.getvalue())
        out = json.loads(out)
        self.assertDictsMatch(
            out[0],
            json.loads(self.FLATPAGE_DUMP),
        )

    def test_serialize_include(self):
        stream = StringIO.StringIO()
        utils.serialize_to_response(app_labels=['sites'], response=stream)
        out = self.normalize(stream.getvalue())
        out = json.loads(out)
        self.assertDictsMatch(
            out[0],
            json.loads(self.SITE_DUMP),
        )

    def test_serialize_unknown_app_fail(self):
        self.assertRaises(CommandError, utils.serialize_to_response, 'auth')

