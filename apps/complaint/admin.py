from django.contrib import admin

# Register your models here.
from apps.complaint.models import Feedback, Complaint


class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by',)
    list_display = ('complaint', 'created_by')

    def save_model(self, request, obj, form, change):
        if obj.id == None:
           obj.created_by = request.user
           super().save_model(request, obj, form, change)

        else:

           super().save_model(request, obj, form, change)


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Complaint)