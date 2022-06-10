from ckeditor.fields import RichTextFormField
from django import forms
from django_select2 import forms as s2forms
from apps.article.models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title','description', 'titleimage','titleimagecaption','category','content','status']
        widgets = {
            'title': forms.TextInput(attrs={'class':'input is-primary','placeholder':'Title'}),
            'description': forms.TextInput(attrs={'cols': 30, 'default': '', 'row': 5, 'class': 'textarea is-primary', 'placeholder': 'Description'}),
            'titleimage': forms.FileInput(attrs={'class': 'file','accept':'image/*', 'type': 'file'}),
            'titleimagecaption': forms.TextInput(attrs={'class': 'input is-primary', 'placeholder': 'Title Image caption'}),
            'category': forms.Select(attrs={'class': 'select is-rounded'}),
            'status': forms.Select(attrs={'class': 'select is-rounded'}),
            'content': RichTextFormField(config_name='default')
        }