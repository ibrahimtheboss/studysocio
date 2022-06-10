from django.db.models import F
from django.template.context_processors import request
from django.test import TestCase
from django.test import Client
from ..forms import *  # import all forms
from ...studysocioprofile.forms import StudySocioProfileForm
from ...studysocioprofile.models import StudySocioProfile


class User_Form_Test(TestCase):

    def setUp(self):
        self.username = "new_user"
        self.email="user@mp.com"
        self.password="qazxcvbnm"
        self.first_name="user"
        self.last_name="user"
        self.designation="Student"

    # Valid Form Data
    def test_UserForm_valid(self):
        signupform = Signup(
            data={'designation': "Student", 'username': self.username, 'email': self.email,
                  'password1': self.password,
                  'password2': self.password, 'first_name': self.first_name,
                  'last_name': self.last_name})
        self.assertTrue(signupform.is_valid())

    # Invalid Form Data

    def test_UserForm_invalid(self):
        form = Signup(data={'username': "user", 'email': "", 'password': "mp", 'first_name': "mp"})
        self.assertFalse(form.is_valid())
