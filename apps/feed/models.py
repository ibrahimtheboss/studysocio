from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone
from emoji_picker.widgets import EmojiPickerTextarea

from apps.topic.models import Topic


class PostFeed(models.Model):
    topic= models.ForeignKey(Topic, related_name='feedtopic', on_delete=models.CASCADE, max_length=150,blank=True, null=True)
    body = models.CharField(max_length=1000)
    feedimage = models.ImageField(upload_to='images/', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='ssuser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created_at',)


class Like(models.Model):
    PostFeed = models.ForeignKey(PostFeed, related_name='likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ReplyFeed(models.Model):
    replybody = models.TextField(max_length=1000)
    postfeed = models.ForeignKey(PostFeed, related_name='replys', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='postuser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('created_at',)


