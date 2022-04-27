from .models import Notification
def notifications(request):
    if request.user.is_authenticated:
        return {'notifications': request.user.notification.filter(is_read=False)}
    else:
        return {'notifications':[]}
            #notifications in html is referance to this