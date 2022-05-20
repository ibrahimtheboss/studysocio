from django.contrib import admin

# Register your models here.
from apps.classroom.models import Classroom, ClassroomMembers, Assignment, LessonMaterials, SubmitAssignment, \
    AssignmentGrades

admin.site.register(Classroom)
admin.site.register(ClassroomMembers)
admin.site.register(Assignment)
admin.site.register(LessonMaterials)
admin.site.register(SubmitAssignment)
admin.site.register(AssignmentGrades)
