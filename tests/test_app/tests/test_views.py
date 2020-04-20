import json
import os.path

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.urls import reverse
from freezegun import freeze_time

from smuggler.forms import ImportForm
from tests.test_app.models import Page


def p(*args):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), *args))


class SuperUserTestCase:
    def setUp(self):
        super().setUp()
        superuser = User(username='superuser')
        superuser.set_password('test')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        self.client.login(username='superuser', password='test')


class TestDumpViewsGenerateDownloadsWithSaneFilenames(SuperUserTestCase,
                                                      TestCase):
    @freeze_time('2012-01-14')
    def test_dump_data(self):
        url = reverse('dump-data')
        response = self.client.get(url)
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename=2012-01-14T00:00:00.json')

    @freeze_time('2012-01-14')
    def test_dump_app_data(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = self.client.get(url)
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename=sites_2012-01-14T00:00:00.json')

    @freeze_time('2012-01-14')
    def test_dump_model_data(self):
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = self.client.get(url)
        self.assertEqual(response['Content-Disposition'],
                         'attachment;'
                         ' filename=sites-site_2012-01-14T00:00:00.json')


class TestDumpData(SuperUserTestCase, TestCase):
    def test_dump_data_parameters(self):
        url = reverse('dump-data')
        response = self.client.get(url, {
            'app_label': 'auth.user,sites'
        })
        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue([i for i in content if i['model'] == 'auth.user'])
        self.assertTrue([i for i in content if i['model'] == 'sites.site'])


class TestDumpHandlesErrorsGracefully(SuperUserTestCase, TestCase):
    def test_erroneous_dump_has_error_messages(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'flatpages'})
        response = self.client.get(url, follow=True)
        response_messages = list(response.context['messages'])
        self.assertEqual(1, len(response_messages))
        self.assertEqual(messages.ERROR, response_messages[0].level)
        self.assertRegex(response_messages[0].message,
                    r'An exception occurred while dumping data:.*flatpages.*')

    def test_erroneous_dump_redirects(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'flatpages'})
        response = self.client.get(url)
        self.assertRedirects(
            response, 'http://testserver/admin/flatpages/',
            target_status_code=404)


class TestLoadDataGet(SuperUserTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('load-data')

    def test_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'smuggler/load_data_form.html')

    def test_has_form_in_context(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'],
                              ImportForm)


class TestLoadDataPost(SuperUserTestCase, TransactionTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('load-data')

    def test_load_fixture(self):
        self.assertEqual(0, Page.objects.count())
        with open(
            p('..', 'smuggler_fixtures', 'page_dump.json'), mode='rb'
        ) as f:
            self.client.post(self.url, {
                'uploads': f
            }, follow=True)
        self.assertEqual(1, Page.objects.count())

    def test_load_fixture_message(self):
        with open(
            p('..', 'smuggler_fixtures', 'page_dump.json'), mode='rb'
        ) as f:
            response = self.client.post(self.url, {
                'uploads': f
            }, follow=True)
        response_messages = list(response.context['messages'])
        self.assertEqual(1, len(response_messages))
        self.assertEqual(messages.INFO, response_messages[0].level)
        self.assertEqual(response_messages[0].message,
                         'Successfully imported 1 file. Loaded 1 object.')

    @override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=0)
    def test_load_fixture_with_chunks(self):
        self.assertEqual(0, Page.objects.count())
        with open(
            p('..', 'smuggler_fixtures', 'big_file.json'), mode='rb'
        ) as f:
            self.client.post(self.url, {
                'uploads': f
            }, follow=True)
        self.assertEqual(1, Page.objects.count())

    def test_handle_garbage_upload(self):
        with open(
            p('..', 'smuggler_fixtures', 'garbage', 'garbage.json'), mode='rb'
        ) as f:
            response = self.client.post(self.url, {
                'uploads': f
            }, follow=True)
        response_messages = list(response.context['messages'])
        self.assertEqual(1, len(response_messages))
        self.assertEqual(messages.ERROR, response_messages[0].level)
        self.assertRegex(response_messages[0].message,
                    'An exception occurred while loading data: '
                    'Problem installing fixture .*')

    def test_handle_integrity_error(self):
        with open(
            p('..', 'smuggler_fixtures', 'garbage', 'invalid_page_dump.json'),
            mode='rb'
        ) as f:
            response = self.client.post(self.url, {
                'uploads': f
            }, follow=True)
        response_messages = list(response.context['messages'])
        self.assertEqual(1, len(response_messages))
        self.assertEqual(messages.ERROR, response_messages[0].level)
        self.assertRegex(response_messages[0].message,
                    r'(?i)An exception occurred while loading data:.*unique.*')

    @override_settings(SMUGGLER_FIXTURE_DIR=p('..', 'smuggler_fixtures'))
    def test_load_from_disk(self):
        self.assertEqual(0, Page.objects.count())
        self.client.post(self.url, {
            'picked_files': p('..', 'smuggler_fixtures', 'page_dump.json')
        }, follow=True)
        self.assertEqual(1, Page.objects.count())

    @override_settings(SMUGGLER_FIXTURE_DIR=p('..', 'smuggler_fixtures'))
    def test_load_from_disk_and_upload(self):
        with open(
            p('..', 'smuggler_fixtures', 'page_dump.json'), mode='rb'
        ) as f:
            response = self.client.post(self.url, {
                'uploads': f,
                'picked_files': p('..', 'smuggler_fixtures', 'page_dump.json')
            }, follow=True)
        response_messages = list(response.context['messages'])
        self.assertEqual(1, len(response_messages))
        self.assertEqual(messages.INFO, response_messages[0].level)
        self.assertEqual(response_messages[0].message,
                         'Successfully imported 2 files. Loaded 2 objects.')

    @override_settings(SMUGGLER_FIXTURE_DIR=p('..', 'smuggler_fixtures'))
    def test_load_and_save(self):
        f = SimpleUploadedFile('uploaded.json',
                               b'[{"pk": 1, "model": "test_app.page",'
                               b' "fields": {"title": "test",'
                               b' "path": "", "body": "test body"}}]')
        self.client.post(self.url, {
            'store': True,
            'uploads': f
        }, follow=True)
        self.assertTrue(os.path.exists(
            p('..', 'smuggler_fixtures', 'uploaded.json')))
        os.unlink(p('..', 'smuggler_fixtures', 'uploaded.json'))
