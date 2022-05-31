from django.contrib import admin

# Register your models here.
from apps.topic.models import Topic

admin.site.register(Topic)