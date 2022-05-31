from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Notification(models.Model):
    MESSAGE = 'message'
    FOLLOWER = 'follower'
    LIKE = 'like'
    MENTION = 'mention'
    REPLY = 'reply'
    LIKE_ARTICLE = 'like_article'
    LIKE_LESSON = 'like_lesson'

    CHOICES = (
        (MESSAGE, 'Message'),
        (FOLLOWER, 'Follower'),
        (LIKE, 'like'),
        (MENTION, 'Mention'),
        (REPLY, 'Reply'),
        (LIKE_ARTICLE, 'like_article'),
        (LIKE_LESSON, 'like_lesson'),
    )

    to_user = models.ForeignKey(User, related_name='notification', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
