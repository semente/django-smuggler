import json
from django.contrib.sites.models import Site
from django.db import IntegrityError
from django.test import TestCase
from smuggler.utils import load_requested_data
from test_app.models import Page


class SimpleLoadTestCase(TestCase):
    PAGE_DUMP = [{
        "pk": 1,
        "model": "test_app.page",
        "fields": {
            "title": "test",
            "body": "test body",
        }
    }]
    SITE_DUMP = [{
        "pk": 1,
        "model": "sites.site",
        "fields": {
            "domain": "example.com",
            "name": "test.com"
        }
    }]
    ALL_DUMP = PAGE_DUMP + SITE_DUMP

    def test_load_page(self):
        self.assertEqual(0, Page.objects.count())
        count = load_requested_data([
            ('json', json.dumps(self.PAGE_DUMP))
        ])
        self.assertEqual(count, 1)
        self.assertEqual('test', Page.objects.get(pk=1).title)

    def test_load_page_and_site(self):
        self.assertEqual(0, Page.objects.count())
        self.assertEqual(Site.objects.get(pk=1).name, 'example.com')
        count = load_requested_data([
            ('json', json.dumps(self.PAGE_DUMP)),
            ('json', json.dumps(self.SITE_DUMP))
        ])
        self.assertEqual(count, 2)
        self.assertEqual('test', Page.objects.get(pk=1).title)
        self.assertEqual('test.com', Site.objects.get(pk=1).name)

    def test_load_all(self):
        self.assertEqual(0, Page.objects.count())
        self.assertEqual(Site.objects.get(pk=1).name, 'example.com')
        count = load_requested_data([
            ('json', json.dumps(self.ALL_DUMP))
        ])
        self.assertEqual(count, 2)
        self.assertEqual('test', Page.objects.get(pk=1).title)
        self.assertEqual('test.com', Site.objects.get(pk=1).name)


class TestInvalidLoad(TestCase):
    PAGE_DUMP = [{
        "pk": 1,
        "model": "test_app.page",
        "fields": {
            "title": "test",
            "path": "",
            "body": "test body",
        },
        "pk": 1,
        "model": "test_app.page",
        "fields": {
            "title": None,
            "body": None,
        }
    }]

    def test_load_invalid_data(self):
        self.assertRaises(IntegrityError, load_requested_data,
                          [('json', json.dumps(self.PAGE_DUMP))])
        self.assertEqual(0, Page.objects.count())
