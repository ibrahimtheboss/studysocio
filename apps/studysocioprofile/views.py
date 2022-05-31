from django.contrib import messages
from django.contrib.auth import user_logged_out, user_logged_in
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import StudySocioProfileForm, EditProfileForm

# Create your views here.
from apps.studysocioprofile.models import FollowRequest, StudySocioProfile
from apps.notification.utilities import create_notification
from ..article.models import Article
from ..feed.models import ReplyFeed, PostFeed
from ..topic.models import Topic
from ..videolessons.models import VideoLesson


@login_required
def studysocioprofile(request, username):
    user = get_object_or_404(User, username=username)
    lessons = VideoLesson.objects.filter(created_by=User.objects.get(username=username), status="Publish")
    articles = Article.objects.filter(created_by=User.objects.get(username=username), status="Publish")
    ssuser = user.ssuser.all()

    for postfeed in ssuser:
        likes = postfeed.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            postfeed.liked = True
        else:
            postfeed.liked = False

    context = {
        'user': user,
        'ssuser': ssuser,
        'lessons':lessons,
        'articles':articles,
    }

    return render(request, 'studysocioprofile/studysocioprofile.html', context)

@login_required
def edit_profile(request):
    if request.method =='POST':
        form1 = EditProfileForm(request.POST, instance=request.user)
        form = StudySocioProfileForm(request.POST, request.FILES, instance=request.user.studysocioprofile)

        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            return redirect('studysocioprofile', username=request.user.username)
    else:
        form = StudySocioProfileForm(instance=request.user.studysocioprofile)
        form1 = EditProfileForm(instance=request.user)

    context = {
        'user': request.user,
        'form': form,
        'form1':form1
    }
    return render(request, 'studysocioprofile/edit_profile.html', context)

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.studysocioprofile.is_online = True
    user.studysocioprofile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.studysocioprofile.is_online = False
    user.studysocioprofile.save()

@login_required
def follow_ssuser(request, username):
    user = get_object_or_404(User, username=username)

    request.user.studysocioprofile.follows.add(user.studysocioprofile)
    create_notification(request, user, 'follower')

    return redirect('studysocioprofile', username=username)


@login_required
def unfollow_ssuser(request, username):
    user = get_object_or_404(User, username=username)

    request.user.studysocioprofile.follows.remove(user.studysocioprofile)

    return redirect('studysocioprofile', username=username)

@login_required
def removefollow_ssuser(request, username):
    user = get_object_or_404(User, username=username)

    request.user.studysocioprofile.followed_by.remove(user.studysocioprofile)

    return redirect('followers', username=request.user.username)# redirect back towrds loggedin's username

def followers(request, username):
    if request.user.username == username :

        user = get_object_or_404(User, username= username)

        return render(request, 'studysocioprofile/followers.html', {'user': user})
    else:
        return redirect('studysocioprofile', username=username)

def follows(request, username):
    if request.user.username == username :

        user = get_object_or_404(User, username= username)

        return render(request, 'studysocioprofile/follows.html', {'user': user})
    else:
        return redirect('studysocioprofile', username=username)







@login_required
def send_friend_request(request, userID):
    user = get_object_or_404(User, id=userID)
    from_user = request.user.studysocioprofile.user
    to_user = user
    followrequest, created = FollowRequest.objects.get_or_create(
        from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('friend request sent')
    else:
        return HttpResponse('friend request was already sent')

@login_required
def accept_friend_request(request, requestID):
    followrequest = FollowRequest.objects.get(id=requestID)
    if followrequest.to_user == request.user.studysocioprofile.user :
        followrequest.to_user.follows.add(followrequest.from_user)
        followrequest.from_user.follows.add(followrequest.to_user)
        followrequest.to_user.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request was not accepted')


##------------------------for the profile view ----------------

@login_required
def deletereplyfeed_profile(request, id, username):
    if request.user.username == username:
        replyfeed = ReplyFeed.objects.get(id=id)  # we need this for both GET and POST

        if request.method == 'POST':
            # delete the feed from the database
            if request.user.studysocioprofile.user == replyfeed.created_by:
                replyfeed.delete()
                # redirect to the feed page
                messages.success(request, 'Successfully Deleted Reply!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # no need for an `else` here. If it's a GET request, just continue

        return render(request, 'studysocioprofile/studysocioprofile.html', {'replyfeed': replyfeed})
    else:
        return redirect('studysocioprofile')


@login_required
def deletefeed_profile(request, id, username):
    if request.user.username == username:
        postfeed = PostFeed.objects.get(id=id)  # we need this for both GET and POST

        if request.method == 'POST':
            # delete the feed from the database
            if request.user.studysocioprofile.user == postfeed.created_by:
                postfeed.delete()
                # redirect to the feed page
                messages.success(request, 'Successfully Deleted!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # no need for an `else` here. If it's a GET request, just continue

        return render(request, 'studysocioprofile/studysocioprofile.html', {'postfeed': postfeed})
    else:
        return redirect('studysocioprofile')

@login_required
def user_articles(request,username):
    user = User.objects.get(username=username)
    articles_list = Article.objects.filter(created_by=User.objects.get(username=username),status="Publish")
    p = Paginator(articles_list, 25)
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        "articles_list": articles_list,
        'page_obj': page_obj,
        'user':user,
    }
    return render(request, 'studysocioprofile/your_articles.html', context)

@login_required
def user_lessons(request,username):
    user = User.objects.get(username=username)
    if user.studysocioprofile.designation == 'Teacher':
        lessons_list = VideoLesson.objects.filter(created_by=User.objects.get(username=username),status="Publish")
        p = Paginator(lessons_list, 25)
        # getting the desired page number from url
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)

        context = {
            "lessons_list": lessons_list,
            'page_obj': page_obj,
            'user':user,
        }
        return render(request, 'studysocioprofile/your_lessons.html', context)
    return redirect('studysocioprofile',username )

