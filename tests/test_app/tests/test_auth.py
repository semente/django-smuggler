from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class TestSmugglerViewsRequireAuthentication(TestCase):
    def test_dump_data(self):
        c = Client()
        url = reverse('dump-data')
        response = c.get(url, follow=True)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/admin/?next=/admin/dump/', 302)])

    def test_dump_app_data(self):
        c = Client()
        url = reverse('dump-app-data', kwargs={'app_label': 'sites'})
        response = c.get(url, follow=True)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/admin/?next=/admin/sites/dump/', 302)])

    def test_dump_model_data(self):
        c = Client()
        url = reverse('dump-model-data', kwargs={
            'app_label': 'sites',
            'model_label': 'site'
        })
        response = c.get(url, follow=True)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/admin/?next=/admin/sites/site/dump/', 302)])

    def test_load_data(self):
        c = Client()
        url = reverse('load-data')
        response = c.get(url, follow=True)
        self.assertEqual(
            response.redirect_chain,
            [('http://testserver/admin/?next=/admin/load/', 302)])


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
