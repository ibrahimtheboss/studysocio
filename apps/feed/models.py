from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone


class PostFeed(models.Model):
    body = models.TextField(max_length=1000)
    feedimage = models.ImageField(upload_to='images/', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='ssuser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created_at',)


class Like(models.Model):
    PostFeed = models.ForeignKey(PostFeed, related_name='likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


