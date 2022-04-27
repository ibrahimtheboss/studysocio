import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PostFeed, Like
from ..notification.utilities import create_notification


@login_required
def api_add_postfeed(request):
    data = json.loads(request.body)
    body = data['body']
    feedimage = data['feedimage']

    postfeed = PostFeed.objects.create(body=body, feedimage=feedimage, created_by=request.user)

    return JsonResponse({'success': True})


@login_required
def api_like_postfeed(request):
    data = json.loads(request.body)
    PostFeed_id = data['PostFeed_id']

    if not Like.objects.filter(PostFeed_id= PostFeed_id).filter(created_by=request.user).exists():
        like = Like.objects.create(PostFeed_id= PostFeed_id, created_by=request.user)
        postfeed = PostFeed.objects.get(pk=PostFeed_id)
        create_notification(request, postfeed.created_by,'like')

    return JsonResponse({'success': True})


def api_display(request):
    userids = [request.user.id]

    for poster in request.user.studysocioprofile.follows.all():
        userids.append(poster.user.id)

    ssuser = PostFeed.objects.filter(created_by_id__in=userids)
    return  JsonResponse({'ssuser': ssuser})

def api_display(request):
    userids = [request.user.id]

    for poster in request.user.studysocioprofile.follows.all():
        userids.append(poster.user.id)

    ssuser = PostFeed.objects.filter(created_by_id__in=userids)
    return  JsonResponse({'ssuser': ssuser})


