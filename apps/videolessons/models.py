from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone
from embed_video.fields import EmbedVideoField

from apps.topic.models import Topic


class VideoLesson(models.Model):
    title = models.CharField(max_length=300)
    Description = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='lessons_images/', blank=True)
    youtube_url = EmbedVideoField(blank=False, null=False)
    category = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="lessoncategory", max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='lesson_creator', on_delete=models.CASCADE)
    STATUS = (
        ('Publish', 'Publish'),
        ('Unpublish', 'Unpublish'),
    )
    status = models.CharField(max_length=10, default='Unpublish', choices=STATUS, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-modified_at']


class Like(models.Model):
    lesson = models.ForeignKey(VideoLesson, related_name='lesson_likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='lesson_likes_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
