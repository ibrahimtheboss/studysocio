import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from .models import Notification

#def getnotification(request):
#    data = Notification.objects.filter(to_user=request.user,is_read=False)
#    #data = request.user.notification.filter(is_read=False)
#    jsonData = serializers.serialize('json', data)
#    return JsonResponse({'data': jsonData})
from django.views import View
from django.http import HttpResponse
@method_decorator(login_required, name='dispatch')
class NotificationCheck(View):
    def get(self, request):
        return HttpResponse(Notification.objects.filter(to_user=request.user,is_read=False).count())