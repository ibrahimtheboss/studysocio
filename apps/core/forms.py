from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User


class Signup(UserCreationForm):
    DESIGNATION = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    )

    designation = forms.CharField(max_length=7,  label='Designation', widget=forms.Select(choices=DESIGNATION))

    class Meta:
        model = User
        fields = ["username", "first_name", 'last_name', "designation", "email", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)

        return self.cleaned_data
