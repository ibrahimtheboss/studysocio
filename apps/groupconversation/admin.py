from django.contrib import admin
from .models import GroupConversation, GroupConversationMessage, GroupConversationMembers

# Register your models here.
admin.site.register(GroupConversation)
admin.site.register(GroupConversationMessage)
admin.site.register(GroupConversationMembers)