from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


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
        self.c = Client()
        self.c.login(username='staff', password='test')

    def test_has_no_load_button(self):
        response = self.c.get(self.url)
        self.assertNotContains(response, '<a href="/admin/load/">')

    def test_has_no_dump_button(self):
        response = self.c.get(self.url)
        self.assertNotContains(response, '<a href="dump/">')


class TestAdminSuperUser(TestCase):
    def setUp(self):
        superuser = User(username='superuser')
        superuser.set_password('test')
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        self.url = reverse('admin:test_app_page_changelist')
        self.c = Client()
        self.c.login(username='superuser', password='test')

    def test_has_load_button(self):
        response = self.c.get(self.url)
        self.assertContains(response, '<a href="/admin/load/">')

    def test_has_dump_button(self):
        response = self.c.get(self.url)
        self.assertContains(response, '<a href="dump/">')
