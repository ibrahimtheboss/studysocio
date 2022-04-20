from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.core.signals import request_finished
from django.dispatch import receiver


# Create your models here.
class FollowRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('p', 'Pending'),
        ('a', 'Accepted'),
        ('r', 'Rejected')
    ]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    timestamp = models.DateTimeField(auto_now_add=True)


class StudySocioProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    bio = models.CharField(max_length=250, blank=True)
    field_of_study = models.CharField(max_length=40, default=' ', blank=True)
    education_center = models.CharField(max_length=60, blank=True)
    DESIGNATION = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin'),
    )
    designation = models.CharField(max_length=7, choices=DESIGNATION, blank=True)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    country = CountryField(blank_label='(select country)')
    avatar = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'


if User != User.is_superuser:
    @receiver(post_save, sender=User)
    def update_studysocioprofile_signal(sender, instance, created, **kwargs):
        if created:
            StudySocioProfile.objects.create(user=instance)
        instance.studysocioprofile.save()

# User.stprofile = property(lambda u:StProfile.objects.get_or_create(user=u)[0])