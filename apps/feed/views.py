import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import PostFeedForm

# Create your views here.

# @login_required
# def feed(request):
#    return render(request, 'feed/feed.html')
from .models import PostFeed
from ..studysocioprofile.models import StudySocioProfile


@login_required
def feed(request):
    if request.user.is_authenticated:
        userids = [request.user.id]

        for poster in request.user.studysocioprofile.follows.all():
            userids.append(poster.user.id)


        ssuser = PostFeed.objects.filter(created_by_id__in=userids)
        context = {
            'ssuser': ssuser,
        }


        for postfeed in ssuser:
            likes = postfeed.likes.filter(created_by_id=request.user.id)

            if likes.count() > 0:
                postfeed.liked = True
            else:
                postfeed.liked = False

        if request.method == 'POST' and not None:

            if 'body' in request.POST:
                body = request.POST['body']
            else:
                body = ''
            if 'feedimage' in request.FILES is not None:
                feedimage = request.FILES['feedimage']
            else:
                feedimage = ''

            postfeed = PostFeed(body=body, feedimage=feedimage, created_by=User.objects.get(pk=request.user.id))
            if postfeed.body is not "" and postfeed.feedimage is not None:
                if postfeed.body == 'go':
                    postfeed.body = 'GO TO BED'
                postfeed.save()
                results = re.findall("(^|[^@\w])@(\w{1,20})", body)

                for result in results:
                    result = result[1]

                    print(result)

                return redirect('feed')
            else:
                return render(request, 'feed/feed.html', context)

        else:
            return render(request, 'feed/feed.html', context)


@login_required
def displayfeed(request):
    userids = [request.user.id]

    for poster in request.user.studysocioprofile.follows.all():
        userids.append(poster.user.id)

    ssuser = PostFeed.objects.filter(created_by_id__in=userids)
    return render(request, 'feed/feed.html', {'ssuser': ssuser})


@login_required
def deletefeed(request, id):
    postfeed = PostFeed.objects.get(id=id)  # we need this for both GET and POST

    if request.method == 'POST':
        # delete the band from the database
        if request.user.studysocioprofile.user == postfeed.created_by:
            postfeed.delete()
            # redirect to the bands list
            return redirect('feed')

        # no need for an `else` here. If it's a GET request, just continue

    return render(request, 'feed/feed.html', {'postfeed': postfeed})


@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        ssusers = User.objects.filter(username__icontains=query)

    else:
        ssusers = []

    context = {
        'query': query,
        'ssusers': ssusers
    }

    return render(request, 'feed/search.html', context)
