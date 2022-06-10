from colorful.fields import RGBColorField
from django.db import models

# Create your models here.
from django.utils import timezone

from apps.core.utils import h_encode


class Topic(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    colour = RGBColorField()
    image = models.ImageField(upload_to='topic_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_hashid(self):
        return h_encode(self.id)

    class Meta:
        ordering = ['name']
