import os.path
from django.contrib.sites.models import Site
from django.test import TestCase, TransactionTestCase
from smuggler.utils import load_fixtures
from tests.test_app.models import Page


p = lambda *args: os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               *args))


class SimpleLoadTestCase(TestCase):
    def test_load_page(self):
        self.assertEqual(0, Page.objects.count())
        count = load_fixtures([
            p('..', 'smuggler_fixtures', 'page_dump.json')])
        self.assertEqual(count, 1)
        self.assertEqual('test', Page.objects.get(pk=1).title)

    def test_load_page_and_site(self):
        self.assertEqual(0, Page.objects.count())
        self.assertEqual(Site.objects.get(pk=1).name, 'example.com')
        count = load_fixtures([
            p('..', 'smuggler_fixtures', 'page_dump.json'),
            p('..', 'smuggler_fixtures', 'site_dump.json')
        ])
        self.assertEqual(count, 2)
        self.assertEqual('test', Page.objects.get(pk=1).title)
        self.assertEqual('test.com', Site.objects.get(pk=1).name)

    def test_load_all(self):
        self.assertEqual(0, Page.objects.count())
        self.assertEqual(Site.objects.get(pk=1).name, 'example.com')
        count = load_fixtures([
            p('..', 'smuggler_fixtures', 'all_dump.json')
        ])
        self.assertEqual(count, 2)
        self.assertEqual('test', Page.objects.get(pk=1).title)
        self.assertEqual('test.com', Site.objects.get(pk=1).name)


class TestInvalidLoad(TransactionTestCase):
    def test_load_invalid_data(self):
        # Would test for IntegrityError but we need to support Django 1.4
        self.assertRaises(Exception, load_fixtures,
                          [p('..', 'smuggler_fixtures',
                             'garbage', 'invalid_page_dump.json')])
        self.assertEqual(0, Page.objects.count())
