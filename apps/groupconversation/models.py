from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class GroupConversation(models.Model):
    name = models.TextField()
    groupimage = models.ImageField(upload_to='group_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,related_name='groupuser', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-modified_at']

class GroupConversationMembers(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    groupconversation = models.ForeignKey(GroupConversation,related_name='groupconversation', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["users", "groupconversation"]


class GroupConversationMessage(models.Model):
    groupconversation = models.ForeignKey(GroupConversation, related_name='groupmessages', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='groupconversation_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='groupmessages', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.groupconversation.save()

        super(GroupConversationMessage, self).save(*args, **kwargs)
@receiver(post_save,sender= GroupConversation)
def addcurrentuserasmemberingroup(sender, instance, created,**kwargs):
    if created:
        #GroupConversationMembers.objects.create(users=instance.created_by,groupconversation=instance.id )
        instance.groupconversation.create(groupconversation=instance.id, users=instance.created_by)
