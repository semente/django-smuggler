import json
import django
from django.utils.six import StringIO
from django.core.management import CommandError
from django.test import TestCase
from tests.test_app.models import Page

from smuggler import utils


class BasicDumpTestCase(TestCase):
    SITE_DICT = {
        "model": "sites.site",
        "fields": {
            "domain": "example.com",
            "name": "example.com"
        }
    }

    if django.VERSION[0:2] < (1, 10):
        SITE_DICT.update({"pk": 1})
    SITE_DUMP = [SITE_DICT]
    PAGE_DUMP = [{
        "pk": 1,
        "model": "test_app.page",
        "fields": {
            "title": "test",
            "path": "",
            "body": "test body",
        }
    }]
    BASIC_DUMP = SITE_DUMP + PAGE_DUMP

    def setUp(self):
        p = Page(title='test', body='test body')
        p.save()

    def normalize(self, out):
        return json.loads(out)

    def test_serialize_exclude(self):
        stream = StringIO()
        utils.serialize_to_response(exclude=['sites', 'auth', 'contenttypes'],
                                    response=stream)
        out = self.normalize(stream.getvalue())
        self.assertEqual(out, self.PAGE_DUMP)

    def test_serialize_include(self):
        stream = StringIO()
        utils.serialize_to_response(app_labels=['sites'], response=stream)
        out = self.normalize(stream.getvalue())
        self.assertEqual(out, self.SITE_DUMP)

    def test_serialize_unknown_app_fail(self):
        self.assertRaises(CommandError, utils.serialize_to_response,
                          ['flatpages'])
