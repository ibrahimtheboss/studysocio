from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField
# Create your models here.
from django.utils import timezone


class Announcement(models.Model):
    title = models.CharField(max_length=300)
    Description = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='announcements_images/', blank=True)
    video = models.FileField(upload_to='announcements_video/', blank=True)
    youtube_url = EmbedVideoField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='announcementscreator', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-modified_at']