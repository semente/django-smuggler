import json
import os.path
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.utils.six.moves import reload_module
from freezegun import freeze_time
from smuggler import settings
from smuggler.forms import ImportFileForm


p = lambda *args: os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               *args))


class SuperUserTestCase(TestCase):
    def setUp(self):
        superuser = User(username='superuser')
        superuser.set_password('test')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        self.c = Client()
        self.c.login(username='superuser', password='test')


class TestDumpViewsGenerateDownloadsWithSaneFilenames(SuperUserTestCase):
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
                         'attachment;'
                         ' filename=sites-site_2012-01-14T00:00:00.json')


class TestDumpData(SuperUserTestCase):
    def test_dump_data_parameters(self):
        url = reverse('dump-data')
        response = self.c.get(url, {
            'app_label': 'auth.user,sites'
        })
        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue([i for i in content if i['model'] == 'auth.user'])
        self.assertTrue([i for i in content if i['model'] == 'sites.site'])


class TestDumpHandlesErrorsGracefully(SuperUserTestCase):
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


class TestLoadDataGet(SuperUserTestCase):
    def setUp(self):
        super(TestLoadDataGet, self).setUp()
        self.url = reverse('load-data')

    def test_renders_correct_template(self):
        response = self.c.get(self.url)
        self.assertEqual('smuggler/load_data_form.html',
                         response.template_name)

    def test_has_form_in_context(self):
        response = self.c.get(self.url)
        self.assertIsInstance(response.context['import_file_form'],
                              ImportFileForm)

    @override_settings(SMUGGLER_FIXTURE_DIR=p('..', 'smuggler_fixtures'))
    def test_has_fixture_dir_in_context(self):
        reload_module(settings)
        response = self.c.get(self.url)
        self.assertEqual(p('..', 'smuggler_fixtures'),
                         response.context['smuggler_fixture_dir'])

    @override_settings(SMUGGLER_FIXTURE_DIR=p('..', 'smuggler_fixtures'))
    def test_has_files_available_in_context(self):
        reload_module(settings)
        response = self.c.get(self.url)
        self.assertEqual([('page_dump.json', '0.1 KB')],
                         response.context['files_available'])

    def tearDown(self):
        reload_module(settings)


class TestLoadDataPost(SuperUserTestCase):
    def setUp(self):
        super(TestLoadDataPost, self).setUp()
        self.url = reverse('load-data')

    def test_empty_fixture(self):
        f = SimpleUploadedFile('valid.json', b'[]')
        response = self.c.post(self.url, {
            '_load': True,
            'file': f
        })
        response_messages = list(response.context['messages'])
        self.assertEqual(1, len(response_messages))
        self.assertEqual(messages.INFO, response_messages[0].level)
        self.assertEqual(
            '0 object(s) from 1 file(s) loaded with success.',
            response_messages[0].message)
