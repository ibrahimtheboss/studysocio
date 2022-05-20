from django.contrib import admin

# Register your models here.
from apps.announcement.models import Announcement

admin.site.register(Announcement)
