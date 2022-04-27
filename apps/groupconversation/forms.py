from django import forms
from django.contrib.auth.models import User
from requests import request

from apps.groupconversation.models import GroupConversation, GroupConversationMembers


class GroupConversationForm(forms.ModelForm):
    class Meta:
        model = GroupConversation
        fields = ('name','groupimage')

class GroupConversationMembersForm(forms.ModelForm):

    class Meta:
        model = GroupConversationMembers

        fields = ('users','groupconversation')

    def __init__(self, *args, **kwargs):
        self.user =kwargs.pop('user', None)
        super(GroupConversationMembersForm, self).__init__(*args, **kwargs)
        self.fields['groupconversation'].queryset = GroupConversation.objects.filter(created_by=self.user)
        Teacher, Student, Admin = 'Teacher', 'Student', 'Admin'
        self.fields['users'].queryset = User.objects.filter(studysocioprofile__designation__in =[Teacher, Student])
    #groupconversation = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)
