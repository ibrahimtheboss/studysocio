from urllib import request

from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from .models import PostFeed
from django.forms import TextInput, ImageField


class PostFeedForm(forms.ModelForm):
    body = forms.CharField()
    body.widget.attrs.update({'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'})

    feedimage = forms.ImageField()
    #feedimage.widget.attrs.update({'placeholder': 'Email', 'style': 'width: 300px;', 'class': 'button',"accept": "image/jpeg"})

    class Meta:
        model = PostFeed
        # PostFeed.feedimage = forms.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg'])])

        fields = ['body', 'feedimage']



