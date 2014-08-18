from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from freezegun import freeze_time


class TestDumpViewsGenerateDownloadsWithSaneFilenames(TestCase):
    def setUp(self):
        superuser = User(username='superuser')
        superuser.set_password('test')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        self.c = Client()
        self.c.login(username='superuser', password='test')

    @freeze_time('2012-01-14')
    def test_dump_data(self):
        url = reverse('dump-data')
        response = self.c.get(url)
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename=2012-01-14T00:00:00.json')

    @freeze_time('2012-01-14')
    def test_dump_app_data(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = self.c.get(url)
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename=sites_2012-01-14T00:00:00.json')

    @freeze_time('2012-01-14')
    def test_dump_model_data(self):
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = self.c.get(url)
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename=sites-site_2012-01-14T00:00:00.json')


class TestDumpHandlesErrorsGracefully(TestCase):
    def setUp(self):
        superuser = User(username='superuser')
        superuser.set_password('test')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        self.c = Client()
        self.c.login(username='superuser', password='test')

    def test_erroneous_dump_has_error_messages(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'flatpages'})
        response = self.c.get(url, follow=True)
        response_messages = list(response.context['messages'])
        self.assertEqual(1, len(response_messages))
        self.assertEqual(messages.ERROR, response_messages[0].level)
        self.assertEqual(
            'An exception occurred while dumping data: '
            'Unknown application: flatpages',
            response_messages[0].message)

    def test_erroneous_dump_redirects(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'flatpages'})
        response = self.c.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('http://testserver/admin/flatpages/',
                         response['location'])
