from django.contrib import admin
from .models import PostFeed, ReplyFeed

# Register your models here.

admin.site.register(PostFeed)
admin.site.register(ReplyFeed)