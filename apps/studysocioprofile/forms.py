from django import forms
from .models import StudySocioProfile

class StudySocioProfileForm(forms.ModelForm):
    class Meta:
        model = StudySocioProfile
        fields = ('avatar','bio','field_of_study','education_center','gender','country','profilestatus')