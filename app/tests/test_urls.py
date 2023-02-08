from django.test import TestCase
from django.urls import reverse, resolve
# Create your tests here.
from django.contrib.auth import get_user
from app.views import profile, index, get_class, index
from django.views.generic import TemplateView

class MyTestCase(TestCase):
    def test_login(self):
        self.client.login(username='fred', password='secret')
        self.assertTrue(get_user(self.client))

    def test_urls(self):
        url = reverse('get_class')
        self.assertEquals(resolve(url).func, get_class)







