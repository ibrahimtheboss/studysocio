from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import StudySocioProfileForm



# Create your views here.
from apps.studysocioprofile.models import FollowRequest, StudySocioProfile


@login_required
def studysocioprofile(request, username):
    user = get_object_or_404(User, username=username)
    ssuser = user.ssuser.all()

    for postfeed in ssuser:
        likes = postfeed.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            postfeed.liked = True
        else:
            postfeed.liked = False

    context = {
        'user': user,
        'ssuser': ssuser
    }

    return render(request, 'studysocioprofile/studysocioprofile.html', context)

@login_required
def edit_profile(request):
    if request.method =='POST':
        form = StudySocioProfileForm(request.POST, request.FILES, instance=request.user.studysocioprofile)

        if form.is_valid():
            form.save()
            return redirect('studysocioprofile', username=request.user.username)
    else:
        form = StudySocioProfileForm(instance=request.user.studysocioprofile)

    context = {
        'user': request.user,
        'form': form
    }
    return render(request, 'studysocioprofile/edit_profile.html', context)


@login_required
def follow_ssuser(request, username):
    user = get_object_or_404(User, username=username)

    request.user.studysocioprofile.follows.add(user.studysocioprofile)

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