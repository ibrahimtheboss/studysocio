import datetime

import kwargs as kwargs
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import utc


class Classroom(models.Model):
    name = models.CharField(max_length=300)
    Description = models.CharField(max_length=300, blank=True, null=True)
    classimage = models.ImageField(upload_to='classimages/', default="../static/img/class_default.jpg", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='classcreator', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-modified_at']


class ClassroomMembers(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, related_name='classroom', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.users}' + " in the class of " + f'{self.classroom}'

    class Meta:
        unique_together = ["users", "classroom"]


@receiver(post_save, sender=Classroom)
def addcurrentuserasmemberinclass(sender, instance, created, **kwargs):
    if created:
        # GroupConversationMembers.objects.create(users=instance.created_by,groupconversation=instance.id )
        instance.classroom.create(classroom=instance.id, users=instance.created_by)


def validate_date(due_date):
    if due_date < timezone.now():
        raise ValidationError("Date cannot be in the past")


class Assignment(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300, null=True, blank=True, )
    assignmentdoc = models.FileField(upload_to='Class_Assignment/', blank=True)
    classroom = models.ForeignKey(Classroom, related_name='assignment', on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True, blank=True, default=None, validators=[validate_date])
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='assignmentcreator', on_delete=models.CASCADE)

    # def get_time_diff(self):
    # if self.time_posted:
    ##now = datetime.datetime.utcnow().replace(tzinfo=utc)
    # timediff = now - self.time_posted
    # return timediff.total_seconds()

    # def updatstatus(self, *args, **kwargs):
    # self.due_date == timezone.now():
    # self.status = 'Closed'
    # super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}' + " in the class of " + f'{self.classroom}'

    class Meta:
        ordering = ['-modified_at']


class LessonMaterials(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, null=True, blank=True, )
    materials = models.FileField(upload_to='Lesson_materials/', blank=True)
    classroom = models.ForeignKey(Classroom, related_name='lessonmaterials', on_delete=models.CASCADE)
    total_marks = models.IntegerField(default=100)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='lessoncreator', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}' + " in the class of " + f'{self.classroom}'

    class Meta:
        ordering = ['-modified_at']


class SubmitAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='submitassignment', on_delete=models.CASCADE)
    description = models.CharField(max_length=300, null=True, blank=True, )
    materials = models.FileField(upload_to='Submitted_Assignment/%Y/%m/%d', blank=False)
    submitted_on_time = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='assignmnetuploader', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.assignment}' + " submitted by " + f'{self.created_by}'

    class Meta:
        ordering = ['-modified_at']
        unique_together = ["assignment", "created_by"]


class AssignmentGrades(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='submitgrades', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='submitassignmentuser', on_delete=models.CASCADE)
    feedback = models.CharField(max_length=300, null=False, blank=False, )
    marks = models.IntegerField(null=True, blank=True, )
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='assignmnetmarker', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.assignment}' + " marks for  " + f'{self.user}' + " with " + f'{self.marks}'

    class Meta:
        ordering = ['-modified_at']
        unique_together = ["assignment",'user', "created_by"]
