from django.contrib import admin
from .models import DirectConversation, DirectConversationMessage
# Register your models here.

admin.site.register(DirectConversation)
admin.site.register(DirectConversationMessage)