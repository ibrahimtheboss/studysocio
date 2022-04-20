from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import StudySocioProfile


@receiver(post_save, sender=User)
def update_studysocioprofile_signal(sender, instance, created, **kwargs):
    if created:
        StudySocioProfile.objects.create(user=instance)
    instance.studysocioprofile.save()
