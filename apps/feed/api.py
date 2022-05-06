import json

from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
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


@login_required
def displayfeed1(request):
    import json
    userids = [request.user.id]

    for poster in request.user.studysocioprofile.follows.all():
        userids.append(poster.user.id)

    ssuser = PostFeed.objects.filter(created_by_id__in=userids)
    postfeed_list = []
    for postfeed in ssuser:

        postfeed_dict = {}
        postfeed_dict['avatar'] =postfeed.created_by.studysocioprofile.avatar.url
        postfeed_dict['username'] = postfeed.created_by.username
        postfeed_dict['created_at'] = postfeed.created_at
        postfeed_dict['body'] = postfeed.body
        postfeed_dict['likes'] = postfeed.likes.count()
        if postfeed.created_by == request.user.studysocioprofile.user:
            postfeed_dict['delete'] = 'delete/'+str(postfeed.id)



        postfeed_list.append(postfeed_dict)

        postfeed_list = list(postfeed_list)



        #data['created_at'] = ssuser
        #data['created_by'] = model_to_dict(ssuser)
        #upload_history =  your orm query  to fetch data
        #json_data = json.dumps( obj_list  )
    return JsonResponse(postfeed_list,safe = False)
        #return HttpResponse( json_data, mimetype='application/json' )


