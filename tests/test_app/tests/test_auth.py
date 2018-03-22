from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestSmugglerViewsRequireAuthentication(TestCase):
    def test_dump_data(self):
        url = reverse('dump-data')
        response = self.client.get(url)
        self.assertRedirects(
            response, '/admin/login/?next=/admin/dump/')

    def test_dump_app_data(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = self.client.get(url)
        self.assertRedirects(
            response, '/admin/login/?next=/admin/sites/dump/')

    def test_dump_model_data(self):
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = self.client.get(url)
        self.assertRedirects(
            response, '/admin/login/?next=/admin/sites/site/dump/')

    def test_load_data(self):
        url = reverse('load-data')
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, '/admin/login/?next=/admin/load/')


class TestSmugglerViewsDeniesNonSuperuser(TestCase):
    def setUp(self):
        staff = User(username='staff')
        staff.set_password('test')
        staff.is_staff = True
        staff.save()
        self.client.login(username='staff', password='test')

    def test_dump_data(self):
        url = reverse('dump-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_dump_app_data(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_dump_model_data(self):
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_load_data(self):
        url = reverse('load-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class TestSmugglerViewsAllowsSuperuser(TestCase):
    def setUp(self):
        superuser = User(username='superuser')
        superuser.set_password('test')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        self.client.login(username='superuser', password='test')

    def test_dump_data(self):
        url = reverse('dump-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dump_app_data(self):
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dump_model_data(self):
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_load_data(self):
        url = reverse('load-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
