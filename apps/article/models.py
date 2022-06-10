

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils import timezone

from apps.core.utils import h_encode
from apps.topic.models import Topic


class Category(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def get_hashid(self):
        return h_encode(self.id)

class Article(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=300,blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    titleimage = models.ImageField(upload_to='titleimages/',default="../static/img/default_article_title_image.png", blank=True)
    titleimagecaption = models.CharField(max_length=300,  blank=True, null=True)
    category = models.ForeignKey(Topic,on_delete=models.CASCADE,related_name="category",max_length=300)
    content = RichTextField(null=True, blank=True,
                            config_name="default", external_plugin_resources=[(
            'youtube', '/static/shareledge/ckeditor-plugins/youtube/youtube/', 'plugin.js',
        )])
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    STATUS = (
        ('Publish', 'Publish'),
        ('Unpublish', 'Unpublish'),
    )
    status = models.CharField(max_length=10, default='Unpublish', choices=STATUS, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-modified_at']

    def get_hashid(self):
        return h_encode(self.id)


class Like(models.Model):
    Article = models.ForeignKey(Article, related_name='article_likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='article_likes_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)