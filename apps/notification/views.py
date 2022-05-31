from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from apps.notification.models import Notification


@login_required
def notifications(request):

    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)




    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('directconversation', user_id=notification.created_by.id)
        elif notification.notification_type == Notification.FOLLOWER:
            return redirect('studysocioprofile', username=notification.created_by.username)
        elif notification.notification_type == Notification.LIKE:
            return redirect('studysocioprofile', username=notification.to_user.username)
        elif notification.notification_type == Notification.MENTION:
            return redirect('studysocioprofile', username=notification.created_by.username)
        elif notification.notification_type == Notification.REPLY:
            return redirect('feed')
        elif notification.notification_type == Notification.LIKE_ARTICLE:
            return redirect('studysocioprofile', username=notification.created_by.username)
        elif notification.notification_type == Notification.LIKE_LESSON:
            return redirect('your_lessons', username=notification.created_by.username)
    return render(request, 'notification/notifications.html')

@login_required
def notificationsclear(request):
    notification = Notification.objects.filter(to_user_id=request.user.id)
    if request.method == 'POST':
        #notification.update(is_read = True)
        notification.delete()
        return redirect('notifications')
    return render(request, 'notification/notifications.html',{'notification': notification})

