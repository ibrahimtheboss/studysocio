from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase
from django.urls import reverse

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'fill',
            'password': 'qazxcvbnm'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)
"""class HomePageTests(SimpleTestCase):
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_url_name(self):
        response = self.client.get(reverse('article'))
        self.assertEquals(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('article'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'article/article.html')"""

""" def test_correct_template_login(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_correct_template_signup(self):
        response = self.client.get('/signup/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')
"""

