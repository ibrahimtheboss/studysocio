from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from apps.core.utils import h_encode


class Complaint(models.Model):
    title = models.CharField(max_length=300)
    Description = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='complaintby', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}' + " by " + f'{self.created_by}'

    class Meta:
        ordering = ['-created_at']
    def get_hashid(self):
        return h_encode(self.id)

class Feedback(models.Model):
    complaint = models.ForeignKey(Complaint, related_name='feedbackto', on_delete=models.CASCADE)
    Description = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)

    def __str__(self):
        return f'{self.complaint}' + " by " + f'{self.created_by}'

    class Meta:
        ordering = ['-created_at']

    def get_hashid(self):
        return h_encode(self.id)
