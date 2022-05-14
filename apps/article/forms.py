from ckeditor.fields import RichTextFormField
from django import forms

from apps.article.models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'titleimage','titleimagecaption','category','content']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'titleimage': forms.TextInput(attrs={'class': 'form-control','accept':'image/*', 'type': 'file','placeholder': 'Image'}),
            'titleimagecaption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title Image caption'}),
            'Category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'content': RichTextFormField(config_name='default')
        }