from unittest import TestCase

from django.contrib.auth.models import User


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

