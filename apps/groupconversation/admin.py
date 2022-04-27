from django.contrib import admin
from .models import GroupConversation,GroupConversationMessage
# Register your models here.
admin.site.register(GroupConversation)
admin.site.register(GroupConversationMessage)