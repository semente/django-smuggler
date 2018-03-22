from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse


class TestAdminNormalUser(TestCase):
    def setUp(self):
        staff = User(username='staff')
        staff.set_password('test')
        staff.is_staff = True
        staff.save()
        staff.user_permissions.add(
            Permission.objects.get_by_natural_key(
                'change_page', 'test_app', 'page'))
        self.url = reverse('admin:test_app_page_changelist')
        self.client.login(username='staff', password='test')

    def test_has_no_load_button(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, '<a href="/admin/load/">')

    def test_has_no_dump_button(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, '<a href="dump/">')


class TestAdminSuperUser(TestCase):
    def setUp(self):
        superuser = User(username='superuser')
        superuser.set_password('test')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        self.url = reverse('admin:test_app_page_changelist')
        self.client.login(username='superuser', password='test')

    def test_has_load_button(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="/admin/load/">')

    def test_has_dump_button(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="dump/">')
