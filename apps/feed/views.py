import re  # regular expressions

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from numpy import argmax

from .forms import PostFeedForm

# Create your views here.

# @login_required
# def feed(request):
#    return render(request, 'feed/feed.html')
from .models import PostFeed, ReplyFeed
from ..notification.utilities import create_notification
from ..studysocioprofile.models import StudySocioProfile
from ..core.m_l_model import imagepredict
from ..topic.models import Topic
from better_profanity import profanity

if __name__ == "__main__":
    profanity.load_censor_words()


"""lines = []
with open('static/words/bad_words_all.txt') as f:
    lines = f.readlines()"""

@login_required
def feed(request):
    if request.user.is_authenticated:
        userids = [request.user.id]

        for poster in request.user.studysocioprofile.follows.all():
            userids.append(poster.user.id)

        ssuser = PostFeed.objects.filter(created_by_id__in=userids)
        for k in ssuser:
            replypost = ReplyFeed.objects.all()
        form = PostFeedForm(request.POST)
        context = {
            'ssuser': ssuser,
            'replypost': replypost,
            'form':form,
        }

        for postfeed in ssuser:
            likes = postfeed.likes.filter(created_by_id=request.user.id)

            if likes.count() > 0:
                postfeed.liked = True
            else:
                postfeed.liked = False

        if request.method == 'POST' and not None :

            if 'body' in request.POST :
                body = request.POST['body']
            else:
                body = ''
            if 'topic' in request.POST :
                topic = request.POST['topic']
            else:
                topic = ''
            if 'feedimage' in request.FILES is not None:
                feedimage = request.FILES['feedimage']
            else:
                feedimage = ''
            if topic == "":
                postfeed = PostFeed( body=body, feedimage=feedimage,created_by=User.objects.get(pk=request.user.id))
            else:
                postfeed = PostFeed(topic=Topic.objects.get(pk=topic), body=body, feedimage=feedimage,created_by=User.objects.get(pk=request.user.id))

            if postfeed.body != "" and postfeed.feedimage !="":
                print(postfeed.feedimage)
                y = imagepredict(postfeed.feedimage)
                if argmax(y) == 0 and float("{:.2f}".format((y[0][0] * 100))) > 85 or argmax(y) == 1 and float("{:.2f}".format((y[0][0] * 100))) > 85:
                    print("The model has predicted the image is MEME" +
                          ' with a Confidence of ' + "{:.2f}".format((y[0][0] * 100)) + '%')
                    messages.warning(request, 'Warning the image uploaded was classified as a prohibited Image')
                    return redirect('feed')

                else:
                    print("good image")

                    cleaned_text = profanity.censor(postfeed.body)
                    postfeed.body = cleaned_text

                    postfeed.save()
                    results = re.findall("(^|[^@\w])@(\w{1,20})", body)
                    for result in results:
                        result = result[1]

                        print(result)
                        # get user form database and do filtering
                        if User.objects.filter(username=result).exists() and result != request.user.username:
                            # creating the notification if someone mentions you, or you mention them
                            create_notification(request, User.objects.get(username=result), 'mention')

                    return redirect('feed')
            elif postfeed.body == "" and postfeed.feedimage !="":
                print(postfeed.feedimage)
                y = imagepredict(postfeed.feedimage)
                if argmax(y) == 0 and float("{:.2f}".format((y[0][0] * 100))) > 85 or argmax(y) == 1 and float("{:.2f}".format((y[0][0] * 100))) > 85:
                    print("The model has predicted the image is MEME" +
                          ' with a Confidence of ' + "{:.2f}".format((y[0][0] * 100)) + '%')
                    messages.warning(request, ' Warning the image uploaded was classified as a prohibited Image')
                    return redirect('feed')

                else:
                    print("good image")
                    postfeed.save()
                    messages.success(request, 'Successfully Posted!!')
                    return redirect('feed')

            elif postfeed.body != "" and postfeed.feedimage is not None:

                cleaned_text = profanity.censor(postfeed.body)
                postfeed.body = cleaned_text
                postfeed.save()
                results = re.findall("(^|[^@\w])@(\w{1,20})", body)
                for result in results:
                    result = result[1]

                    print(result)
                    # get user form database and do filtering
                    if User.objects.filter(username=result).exists() and result != request.user.username:
                        # creating the notification if someone mentions you, or you mention them
                        create_notification(request, User.objects.get(username=result), 'mention')
                messages.success(request, 'Successfully Posted!!')
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
        # delete the feed from the database
        if request.user.studysocioprofile.user == postfeed.created_by:
            postfeed.delete()
            # redirect to the feed page
            messages.success(request, 'Successfully Deleted!!')
            return redirect('feed')

        # no need for an `else` here. If it's a GET request, just continue

    return render(request, 'feed/feed.html', {'postfeed': postfeed})


@login_required
def replypost(request):
    # replypost = ReplyFeed.objects.filter(postfeed=id)  # we need this for both GET and POST
    if request.user.is_authenticated:

        if request.method == 'POST':
            if 'replybody' in request.POST:
                replybody = request.POST['replybody']
                postfeed = request.POST['postfeed']

            else:
                replybody = ''
                postfeed = ''

            reply = ReplyFeed.objects.create(replybody=replybody, postfeed=PostFeed.objects.get(id=postfeed),
                                             created_by=User.objects.get(pk=request.user.id))
            reply.save()
            user = reply.postfeed.created_by
            if user != request.user:
                create_notification(request, user, 'reply')
            # redirect to the feed page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # no need for an `else` here. If it's a GET request, just continue

    return render(request, 'feed/feed.html')

@login_required
def deletereplyfeed(request, id):
    replyfeed = ReplyFeed.objects.get(id=id)  # we need this for both GET and POST

    if request.method == 'POST':
        # delete the feed from the database
        if request.user.studysocioprofile.user == replyfeed.created_by:
            replyfeed.delete()
            # redirect to the feed page
            messages.success(request, 'Successfully Deleted Reply!!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # no need for an `else` here. If it's a GET request, just continue

    return render(request, 'feed/feed.html', {'replyfeed': replyfeed})




@login_required
def viewreplypost(request, id):
    if request.user.is_authenticated:
        # replypost = ReplyFeed.objects.filter(postfeed=id)  # we need this for both GET and POST
        j = ReplyFeed.objects.get(postfeed=id)
        h = j
        return render(request, 'feed/feed.html', {'h': h})
        # redirect to the feed page

    # no need for an `else` here. If it's a GET request, just continue


@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        Teacher, Student, Admin = 'Teacher', 'Student', 'Admin'

        ssusers = User.objects.filter(username__icontains=query)
        ssusers = ssusers.filter(studysocioprofile__designation__in=[Teacher, Student])

        postfeed = PostFeed.objects.filter(body__icontains='#' + query)

    else:
        ssusers = []
        postfeed = []

    context = {
        'query': query,
        'ssusers': ssusers,
        'postfeed': postfeed
    }

    return render(request, 'feed/search.html', context)


