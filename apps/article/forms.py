from ckeditor.fields import RichTextFormField
from django import forms
from django_select2 import forms as s2forms
from apps.article.models import Article

class CategoryWidget(s2forms.ModelSelect2Widget):
    empty_label = 'False'
    search_fields = [
        "name__icontains",
    ]

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'titleimage','titleimagecaption','category','content']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'titleimage': forms.TextInput(attrs={'class': 'form-control','accept':'image/*', 'type': 'file','placeholder': 'Image'}),
            'titleimagecaption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title Image caption'}),
            'category': CategoryWidget(),
            'content': RichTextFormField(config_name='default')
        }