from urllib import request

from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from emoji_picker.widgets import EmojiPickerTextarea, EmojiPickerTextareaAdmin

from .models import PostFeed
from django.forms import TextInput, ImageField



class PostFeedForm(forms.ModelForm):
    class Meta:
        model = PostFeed
        fields = ['body','topic']
        widgets = {
            'topic': forms.Select(attrs={'name':"topic", "id":"topic", 'placeholder': 'Topic'}),
            'body':EmojiPickerTextarea(attrs={ 'cols': 80, 'default':'','row':25,'class': 'textarea is-primary','name':"body", "id":"body", 'placeholder': 'What are you Posting?'})
        }





