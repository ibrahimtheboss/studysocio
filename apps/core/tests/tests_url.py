from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_url_name(self):
        response = self.client.get(reverse('frontpage'))
        self.assertEquals(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('frontpage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/frontpage.html')

    def test_correct_template_login(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_correct_template_signup(self):
        response = self.client.get('/signup/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')