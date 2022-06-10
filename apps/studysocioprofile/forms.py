from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import StudySocioProfile


class StudySocioProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = StudySocioProfile
        fields = ('avatar','bio', 'field',
                  'education_center', 'gender', 'country', 'profilestatus', 'background_image')



        widgets = {
            'avatar': forms.ClearableFileInput(
                attrs={"label": "Foo", 'class': 'file is-primary', 'accept': 'image/*', 'type': 'file'}),
            'background_image': forms.ClearableFileInput(
                attrs={'class': 'file is-primary', 'accept': 'image/*', 'type': 'file'}),
            'bio': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'About yourself , interest on research '
                                                                             'Study, Education etc.'}),
            'field': forms.TextInput(attrs={'class': 'input',
                                                        'placeholder': 'Eg: Civil Engineering ,Computer Science'                                                                             'Discipline '}),
            'education_center': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Eg: University of Cambridge'}),
            'gender': forms.Select(attrs={'class': 'select is-rounded'}),
            'country': forms.Select(attrs={'class': 'select is-rounded'}),
            'profilestatus': forms.Select(attrs={'class': 'select is-rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudySocioProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].label = "Profile Picture"
        self.fields['background_image'].label = "Profile Background Image"
        self.fields['bio'].label = "Bio"
        self.fields['field'].label = "Field"
        self.fields['education_center'].label = "Education Center"
        self.fields['gender'].label = "Gender"
        self.fields['country'].label = "Country"
        self.fields['profilestatus'].label = "Profile Status"



class EditProfileForm(ModelForm):
    class Meta:

        model = User
        fields = (
            'email',
            'first_name',
            'last_name'
        )
