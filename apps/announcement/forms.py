
from ckeditor.fields import RichTextFormField
from django import forms
from django_select2 import forms as s2forms
from embed_video.fields import EmbedVideoField, EmbedVideoFormField

from apps.announcement.models import Announcement


class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ['title','Description', 'image','video','youtube_url']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'Description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'file','accept':'image/*', 'type': 'file'}),
            'video': forms.FileInput(attrs={'class': 'file', 'accept': 'video/mp4', 'type': 'file'}),
        }
