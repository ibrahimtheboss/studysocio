from ckeditor.fields import RichTextFormField
from django import forms
from django_select2 import forms as s2forms
from embed_video.fields import EmbedVideoField, EmbedVideoFormField

from apps.announcement.models import Announcement
from apps.videolessons.models import VideoLesson


class VideoLessonForm(forms.ModelForm):

    class Meta:
        model = VideoLesson
        fields = ['title','Description','category','image','youtube_url','status']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'Description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'file','accept':'image/*', 'type': 'file'}),
        }
