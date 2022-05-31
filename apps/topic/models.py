from colorful.fields import RGBColorField
from django.db import models

# Create your models here.
from django.utils import timezone


class Topic(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    colour = RGBColorField()
    image = models.ImageField(upload_to='topic_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']