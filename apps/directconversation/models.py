from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class DirectConversation(models.Model):
    users = models.ManyToManyField(User, related_name='directconversations')
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']

class DirectConversationMessage(models.Model):
    directconversation = models.ForeignKey(DirectConversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='conversation_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.directconversation.save()

        super(DirectConversationMessage, self).save(*args, **kwargs)


