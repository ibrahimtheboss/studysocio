import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from apps.classroom.forms import ClassroomForm, ClassroomMembersForm, AssignmentGradesForm, AssignmentForm, \
    SubmitAssignmentForm, LessonMaterialsForm
from apps.classroom.models import Classroom, ClassroomMembers, Assignment, AssignmentGrades, SubmitAssignment, \
    LessonMaterials


@login_required
def classrooms(request):
    classrooms = ClassroomMembers.objects.filter(users=request.user)

    return render(request, 'classroom/classroom.html', {'classrooms': classrooms})

@login_required
def classroom_activity(request,classroom_id):
    classroom_details = Classroom.objects.filter(id=classroom_id)
    lesson_materials = LessonMaterials.objects.filter(classroom=classroom_id)
    classroom_members = ClassroomMembers.objects.filter(classroom=classroom_id)
    classroom_assignment = Assignment.objects.filter(classroom=classroom_id)
    submit_assignments = SubmitAssignment.objects.filter(created_by= request.user)

    context = {
        'classroom_details': classroom_details,
        'lesson_materials':lesson_materials,
        'classroom_members': classroom_members,
        'classroom_assignment': classroom_assignment,
        'submit_assignments':submit_assignments,
    }
    return render(request, 'classroom/classroom_activity.html', context)

@login_required
def create_classroom(request):

    if request.method == 'POST':
        form = ClassroomForm(request.POST, request.FILES)

        if form.is_valid():
            classroom = Classroom.objects.create(

                created_by=User.objects.get(pk=request.user.id),
                name=form.cleaned_data["name"],
                Description=form.cleaned_data["Description"],
                classimage=form.cleaned_data["classimage"],
            )


            classroom.save()

            return redirect('create_classroom')
    else:
        form = ClassroomForm()
        return render(request, "classroom/create_classroom.html", {'form': form})

@login_required
def edit_classroom(request, classroom_id):
    obj = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ClassroomForm(instance=obj)

    context = {
        'obj': obj,
        'form': form
    }
    return render(request, "classroom/edit_classroom.html", context)

@login_required
def delete_classroom(request,classroom_id):
    classrooms = ClassroomMembers.objects.filter(users=request.user)
    classroom_members = ClassroomMembers.objects.filter(classroom=classroom_id)
    classroom = Classroom.objects.filter(id=classroom_id)

    context = {
        'classrooms':classrooms,
    }
    if request.method == 'POST':
        classroom_members.delete()
        classroom.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'classroom/classroom.html', context)


@login_required
def add_classroom_members(request,classroom_id):
    obj = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = ClassroomMembersForm(request.POST)

        if form.is_valid():
            try:
                members = ClassroomMembers.objects.create(
                    classroom=Classroom.objects.get(pk=classroom_id),
                    users=form.cleaned_data["users"],
                )

                members.save()
                messages.success(request, 'successfully Added user to group.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            except IntegrityError:
                messages.warning(request, 'This user already exists.')
        else:
            return render(request, 'classroom/add_classroom_members.html',
                          {'form': form,
                           })
    else:
        form = ClassroomMembersForm()

    context = {
        'obj':obj,
        'form': form,
    }
    return render(request, 'classroom/add_classroom_members.html', context)
@login_required
def remove_classroom_members(request,classroom_id,user_id):
    classroom_details = Classroom.objects.filter(id=classroom_id)
    classroom_members = ClassroomMembers.objects.filter(classroom=classroom_id)
    classroom_assignment = Assignment.objects.filter(classroom=classroom_id)
    lesson_materials = LessonMaterials.objects.filter(classroom=classroom_id)
    classrooms = ClassroomMembers.objects.filter(users=request.user)
    classroom_members = ClassroomMembers.objects.filter(classroom=classroom_id)
    classroom = Classroom.objects.filter(id=classroom_id)

    remove_ass_sub = SubmitAssignment.objects.filter(created_by=user_id)
    remove_grade = AssignmentGrades.objects.filter(user=user_id)
    remove_member = ClassroomMembers.objects.filter(users=user_id,classroom=classroom_id)


    context = {
        'classrooms':classrooms,
        'classroom_details':classroom_details,
        'lesson_materials':lesson_materials,
        'classroom_members': classroom_members,
        'classroom_assignment': classroom_assignment,
    }
    if request.method == 'POST':
        remove_grade.delete()
        remove_ass_sub.delete()
        remove_member.delete()

        messages.success(request, 'successfully Removed')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'classroom/classroom_activity.html', context)


@login_required
def leave_classroom(request,classroom_id):
    classrooms = ClassroomMembers.objects.filter(users=request.user)
    leave_classrooms = ClassroomMembers.objects.filter(classroom=classroom_id,users=request.user)


    context = {
        'classrooms':classrooms,
    }
    if request.method == 'POST':
        leave_classrooms.delete()
        messages.success(request, 'successfully Left the classroom.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'classroom/classroom.html', context)





@login_required
def add_classroom_assignment(request,classroom_id):
    obj = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                members = Assignment.objects.create(
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                    assignmentdoc=form.cleaned_data["assignmentdoc"],
                    classroom=Classroom.objects.get(pk=classroom_id),
                    due_date=form.cleaned_data["due_date"],
                    total_marks=form.cleaned_data["total_marks"],
                    created_by=User.objects.get(pk=request.user.id),
                    status=form.cleaned_data["status"]
                )

                members.save()
                messages.success(request, 'successfully Added Assignment to Classroom.')
                return render(request, 'classroom/create_assignment.html',
                              {'form': form,
                               })

            except IntegrityError:
                messages.warning(request, 'error')

        else:
            return render(request, 'classroom/create_assignment.html',
                          {'form': form,
                           })
    else:
        form = AssignmentForm()

    context = {
        'obj':obj,
        'form': form,
        }
    return render(request, 'classroom/create_assignment.html', context)
@login_required
def edit_classroom_assignment(request,classroom_id, assignment_id):
    obj = Classroom.objects.get(id=classroom_id)
    assign_obj = Assignment.objects.get(id=assignment_id,classroom=classroom_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assign_obj)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = AssignmentForm(instance=assign_obj)

    context = {
        'obj': obj,
        'form': form
    }
    return render(request, "classroom/edit_assignment.html", context)


@login_required
def delete_classroom_assignment(request,classroom_id,assignment_id):
    classroom_details = Classroom.objects.filter(id=classroom_id)
    classroom_members = ClassroomMembers.objects.filter(classroom=classroom_id)
    classroom_assignment = Assignment.objects.filter(classroom=classroom_id)
    lesson_materials = LessonMaterials.objects.filter(classroom=classroom_id)
    classrooms = ClassroomMembers.objects.filter(users=request.user)
    classroom_members = ClassroomMembers.objects.filter(classroom=classroom_id)
    classroom = Classroom.objects.filter(id=classroom_id)

    """del_sub_assignment = SubmitAssignment.objects.get(assignment=assignment_id)
    del_grade_assignment = AssignmentGrades.objects.get(assignment=assignment_id)"""
    del_assignment = Assignment.objects.get(id=assignment_id)


    context = {
        'classrooms':classrooms,
        'classroom_details':classroom_details,
        'lesson_materials':lesson_materials,
        'classroom_members': classroom_members,
        'classroom_assignment': classroom_assignment,
    }
    if request.method == 'POST':
        del_assignment.delete()

        messages.success(request, 'successfully Deleted Assignment')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'classroom/classroom_activity.html', context)



@login_required
def add_assignment_grades(request,classroom_id,assignment_id):
    #User.objects.filter(id__in=ClassroomMembers.objects.filter(users__classroom__created_by__in=self.user))
    """k = ClassroomMembers.objects.filter(classroom=15)
    k= User.objects.filter(classroommembers__id__in=k)"""
    if request.method == 'POST':
        form = AssignmentGradesForm(request.POST,  request.FILES,classroom=classroom_id,user=request.user)

        if form.is_valid():
            try:
                grade = AssignmentGrades.objects.create(

                    created_by=User.objects.get(pk=request.user.id),
                    assignment=Assignment.objects.get(pk=assignment_id),
                    user=form.cleaned_data["user"],
                    feedback=form.cleaned_data["feedback"],
                    marks=form.cleaned_data["marks"],
                )

                # user_id = request.POST.get('users')
                # user = User.objects.get(id=user_id)
                grade.save()
                # GroupConversationMembers.objects.create(users=request.user,groupconversation=request.groupconversation__set.id)

                # groupconversation.users.set(user)
                messages.success(request, 'successfully Added Results to Assignment')

                return redirect('classroom_activity',classroom_id)

            except IntegrityError:
                messages.warning(request, 'User has Already been given results.')
        else:
            form = AssignmentGradesForm(classroom=classroom_id, user=request.user)
            return render(request, "classroom/add_assignment_grades.html",
                          {'form': form,
                           })
    else:
        form = AssignmentGradesForm(classroom=classroom_id,user=request.user)
    return render(request, "classroom/add_assignment_grades.html", {'form': form})
@login_required
def edit_assignment_grades(request,classroom_id, assignment_id,assignment_grade_id):
    obj = Classroom.objects.get(id=classroom_id)
    assign_obj = AssignmentGrades.objects.get(id=assignment_grade_id)
    if request.method == 'POST':
        form = AssignmentGradesForm(request.POST, request.FILES, classroom=classroom_id,user=request.user,instance=assign_obj)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = AssignmentGradesForm(classroom=classroom_id,user=request.user,instance=assign_obj)

    context = {
        'obj': obj,
        'form': form
    }
    return render(request, "classroom/edit_assignment_grades.html", context)



@login_required
def submit_assignment(request,classroom_id,assignment_id):
    obj = Classroom.objects.get(id=classroom_id)
    sub_valid = Assignment.objects.get(pk=assignment_id)
    if sub_valid.due_date > timezone.now():
        time_value =True
    else:
        time_value= False
    if request.method == 'POST':
        form = SubmitAssignmentForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                sub_assign = SubmitAssignment.objects.create(
                    assignment=Assignment.objects.get(pk=assignment_id),
                    description=form.cleaned_data["description"],
                    materials=form.cleaned_data["materials"],
                    submitted_on_time=time_value,
                    created_by=User.objects.get(pk=request.user.id),
                )

                sub_assign.save()
                messages.success(request, 'successfully Submitted Assignment to Classroom.')
                return redirect('classroom_activity',classroom_id)

            except IntegrityError:
                messages.warning(request, 'You have already Submitted!!')

        else:
            return render(request, 'classroom/submit_assignment.html',
                          {'form': form,
                           })
    else:
        form = SubmitAssignmentForm()

    context = {
        'obj':obj,
        'form': form,
        }
    return render(request, 'classroom/submit_assignment.html', context)

@login_required
def view_submit_assignment(request,classroom_id,assignment_id):
    submit_assignments_by_student = SubmitAssignment.objects.filter(assignment=assignment_id,created_by= request.user)
    grades_assignments_by_student = AssignmentGrades.objects.filter(assignment=assignment_id, user=request.user)
    submit_assignments_for_teacher = SubmitAssignment.objects.filter(assignment=assignment_id)
    grades_assignments_for_teacher = AssignmentGrades.objects.filter(assignment=assignment_id)
    ass_detail = Assignment.objects.filter(id=assignment_id)
    current_datetime = datetime.datetime.now()

    context = {
        'submit_assignments_by_student': submit_assignments_by_student,
        'submit_assignments_for_teacher':submit_assignments_for_teacher,
        'grades_assignments_by_student': grades_assignments_by_student,
        'grades_assignments_for_teacher': grades_assignments_for_teacher,
        'ass_detail': ass_detail,
        'current_datetime':current_datetime,

    }
    return render(request, 'classroom/view_assignment.html', context)


@login_required
def edit_submit_assignment(request,classroom_id,assignment_id, submitassign_id):
    obj = Classroom.objects.get(id=classroom_id)
    assign_obj = SubmitAssignment.objects.get(id=submitassign_id,assignment=assignment_id)
    if request.method == 'POST':
        form = SubmitAssignmentForm(request.POST, request.FILES, instance=assign_obj)

        if form.is_valid():
            form.save()
            messages.success(request, 'successfully Updated Submitted Assignment to Classroom.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = SubmitAssignmentForm(instance=assign_obj)

    context = {
        'obj': obj,
        'form': form
    }
    return render(request, "classroom/edit_submit_assignment.html", context)

@login_required
def add_lesson_materials(request,classroom_id):
    #User.objects.filter(id__in=ClassroomMembers.objects.filter(users__classroom__created_by__in=self.user))
    """k = ClassroomMembers.objects.filter(classroom=15)
    k= User.objects.filter(classroommembers__id__in=k)"""
    if request.method == 'POST':
        form = LessonMaterialsForm(request.POST, request.FILES)

        if form.is_valid():
            classroom_lesson = LessonMaterials.objects.create(

                created_by=User.objects.get(pk=request.user.id),
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                materials=form.cleaned_data["materials"],
                classroom=Classroom.objects.get(pk=classroom_id)
            )
            classroom_lesson.save()
            messages.success(request, 'successfully Uploaded Lesson Materials to Classroom.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'An error occurred !!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = LessonMaterialsForm()
        return render(request, "classroom/add_lesson_materials.html", {'form': form})

@login_required
def edit_lesson_materials(request, classroom_id,lesson_materials_id):
    obj = LessonMaterials.objects.get(id=lesson_materials_id)
    if request.method == 'POST':
        form = LessonMaterialsForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(request, 'successfully Edited Lesson Materials to Classroom.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'An error occurred !!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = LessonMaterialsForm(instance=obj)

    context = {
        'obj': obj,
        'form': form
    }
    return render(request, "classroom/edit_lesson_materials.html", context)


@login_required
def delete_lesson_materials(request,classroom_id,lesson_materials_id):
    classroom_details = Classroom.objects.filter(id=classroom_id)
    lesson_materials = LessonMaterials.objects.filter(classroom=classroom_id)
    classrooms = ClassroomMembers.objects.filter(users=request.user)
    classroom_members = ClassroomMembers.objects.filter(classroom=classroom_id)
    classroom = Classroom.objects.filter(id=classroom_id)
    del_lesson_materials = LessonMaterials.objects.get(id=lesson_materials_id)

    context = {
        'classrooms':classrooms,
        'classroom_details':classroom_details,
        'lesson_materials':lesson_materials,
    }
    if request.method == 'POST':
        del_lesson_materials.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'classroom/classroom_activity.html', context)

