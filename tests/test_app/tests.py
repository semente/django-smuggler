import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.six import StringIO
from django.core.management import CommandError
from django.test import TestCase, Client
from test_app.models import Page
from smuggler import utils


class BasicDumpTestCase(TestCase):
    SITE_DUMP = [{
        "pk": 1,
        "model": "sites.site",
        "fields": {
            "domain": "example.com",
            "name": "example.com"
        }
    }]
    PAGE_DUMP = [{
        "pk": 1,
        "model": "test_app.page",
        "fields": {
            "title": "test", "body": "test body",
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


class TestSmugglerUrls(TestCase):
    def test_can_reverse_dump_data(self):
        self.assertEqual(reverse('dump-data'), '/admin/dump/')

    def test_can_reverse_dump_app_data(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        self.assertEqual(url, '/admin/sites/dump/')

    def test_can_reverse_dump_model_data(self):
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        self.assertEqual(url, '/admin/sites/site/dump/')

    def test_can_reverse_load_data(self):
        self.assertEqual(reverse('load-data'), '/admin/load/')


class TestSmugglerViewsRequireAuthentication(TestCase):
    def test_dump_data(self):
        c = Client()
        url = reverse('dump-data')
        response = c.get(url, follow=True)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/login/?next=/admin/dump/', 302)])

    def test_dump_app_data(self):
        c = Client()
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = c.get(url, follow=True)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/login/?next=/admin/sites/dump/', 302)])

    def test_dump_model_data(self):
        c = Client()
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = c.get(url, follow=True)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/login/?next=/admin/sites/site/dump/', 302)])

    def test_load_data(self):
        c = Client()
        url = reverse('load-data')
        response = c.get(url, follow=True)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/accounts/login/?next=/admin/load/', 302)])


class TestSmugglerViewsDeniesNonSuperuser(TestCase):
    def setUp(self):
        staff = User(username='staff')
        staff.set_password('test')
        staff.is_staff = True
        staff.save()

    def test_dump_data(self):
        c = Client()
        c.login(username='staff', password='test')
        url = reverse('dump-data')
        response = c.get(url)
        self.assertEqual(response.status_code, 403)

    def test_dump_app_data(self):
        c = Client()
        c.login(username='staff', password='test')
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = c.get(url)
        self.assertEqual(response.status_code, 403)

    def test_dump_model_data(self):
        c = Client()
        c.login(username='staff', password='test')
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = c.get(url)
        self.assertEqual(response.status_code, 403)

    def test_load_data(self):
        c = Client()
        c.login(username='staff', password='test')
        url = reverse('load-data')
        response = c.get(url)
        self.assertEqual(response.status_code, 403)


class TestSmugglerViewsAllowsSuperuser(TestCase):
    def setUp(self):
        superuser = User(username='superuser')
        superuser.set_password('test')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()

    def test_dump_data(self):
        c = Client()
        c.login(username='superuser', password='test')
        url = reverse('dump-data')
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dump_app_data(self):
        c = Client()
        c.login(username='superuser', password='test')
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dump_model_data(self):
        c = Client()
        c.login(username='superuser', password='test')
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_load_data(self):
        c = Client()
        c.login(username='superuser', password='test')
        url = reverse('load-data')
        response = c.get(url)
        self.assertEqual(response.status_code, 200)