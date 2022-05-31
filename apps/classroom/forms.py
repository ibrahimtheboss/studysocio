from datetimepicker.widgets import DateTimePicker
from django import forms
from django.contrib.auth.models import User
from django.http import request
from django_select2 import forms as s2forms
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from apps.classroom.models import Classroom, ClassroomMembers, Assignment, SubmitAssignment, AssignmentGrades, \
    LessonMaterials


class UserWidget(s2forms.ModelSelect2Widget):
    empty_label = 'False'
    search_fields = [
        "username__icontains",
    ]


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'Description', 'classimage']


class ClassroomMembersForm(forms.ModelForm):
    class Meta:
        model = ClassroomMembers
        fields = ['users',]
        widgets = {
            'users': UserWidget(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ClassroomMembersForm, self).__init__(*args, **kwargs)
        #self.fields['classroom'].queryset = Classroom.objects.filter(created_by=self.user)
        Teacher, Student, Admin = 'Teacher', 'Student', 'Admin'
        self.fields['users'].queryset = User.objects.filter(studysocioprofile__designation__in=[Teacher, Student])

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['name','description','assignmentdoc','due_date','total_marks','status']
        widgets = {
            'due_date': DateTimePickerInput(),
            'total_marks': forms.TextInput()
        }


class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ['description', 'materials',]


class AssignmentGradesForm(forms.ModelForm):
    class Meta:
        model = AssignmentGrades
        fields = ['classroom','user','feedback', 'marks',]
        exclude = ['assignment','classroom',]

    """def __init__(self, request, classroom_id, *args, **kwargs):
        k = ClassroomMembers.objects.filter(classroom=classroom_id)
        k = User.objects.filter(classroommembers__id__in=k)
        self.request = request
        super(AssignmentGradesForm, self).__init__(*args, **kwargs)
        self.fields['assignment'].queryset = Assignment.objects.filter(created_by_id=self.request)
        self.fields['user'].queryset= k"""


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.classroom = kwargs.pop('classroom', None)
        #self.request = request

        super(AssignmentGradesForm, self).__init__(*args, **kwargs)
        #self.fields['assignment'].queryset = Assignment.objects.filter(created_by_id=self.user)
        k = ClassroomMembers.objects.filter(classroom=self.classroom)
        k = User.objects.filter(classroommembers__id__in=k)
        self.fields['user'].queryset = k



class LessonMaterialsForm(forms.ModelForm):
    class Meta:
        model = LessonMaterials
        fields = ['name', 'description','materials']