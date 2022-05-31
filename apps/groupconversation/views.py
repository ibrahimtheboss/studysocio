import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from numpy import argmax

from apps.core.m_l_model import imagepredict
from apps.directconversation.models import DirectConversationMessage
from apps.groupconversation.forms import GroupConversationForm, GroupConversationMembersForm
from apps.groupconversation.models import GroupConversation, GroupConversationMembers, GroupConversationMessage

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupConversationForm(request.POST, request.FILES)
        if form.is_valid():
            groupconversation = GroupConversation.objects.create(

                created_by=User.objects.get(pk=request.user.id),
                name=form.cleaned_data["name"],
                groupimage=form.cleaned_data["groupimage"],
            )

            # user_id = request.POST.get('users')
            # user = User.objects.get(id=user_id)
            groupconversation.save()
            # GroupConversationMembers.objects.create(users=request.user,groupconversation=request.groupconversation__set.id)

            # groupconversation.users.set(user)

            return redirect('create_group')
    else:
        form = GroupConversationForm()
        return render(request, "groupconversation/create_group.html", {'form': form})

@login_required
def edit_group(request, id):
    obj = GroupConversation.objects.get(id=id)
    if request.method == 'POST':
        form = GroupConversationForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = GroupConversationForm(instance=obj)

    context = {
        'obj': obj,
        'form': form
    }
    return render(request, 'groupconversation/edit_group.html', context)

@login_required
def add_member(request,group_id):
    obj = GroupConversation.objects.get(id=group_id)
    if request.method == 'POST':
        form = GroupConversationMembersForm(request.POST)

        if form.is_valid():
            try:
                group = GroupConversationMembers.objects.create(
                    groupconversation=GroupConversation.objects.get(pk=group_id),
                    users=form.cleaned_data["users"],
                )

                group.save()
                messages.success(request, 'sucessfully Added user to group.')
                return render(request, 'groupconversation/add_members.html',
                              {'form': form,
                               })

            except IntegrityError:
                messages.warning(request, 'This user already exists.')
        else:
            return render(request, 'groupconversation/add_members.html',
                          {'form': form,
                           })
    else:
        form = GroupConversationMembersForm()

    context = {
        'obj':obj,
        'form': form,
    }
    return render(request, 'groupconversation/add_members.html', context)


@login_required
def groupconversations(request):
    groupconversations = GroupConversationMembers.objects.all()
    # groupconversations = groupconversations.filter(messages =F('messages')).distinct() # here we filter if coversation id  is in messages Fk coversatio nid

    return render(request, 'groupconversation/groupconversations.html', {'groupconversations': groupconversations})


@login_required
def groupconversation(request, group_id):
    try:
        groupmembers = GroupConversationMembers.objects.get(groupconversation=group_id, users=request.user)
    except GroupConversationMembers.DoesNotExist:
        raise Http404("Post not found")
    if request.user.is_authenticated and groupmembers:
        groupconversation = GroupConversationMessage.objects.filter(groupconversation=group_id)
        groupconversationmembers = GroupConversationMembers.objects.filter(groupconversation=group_id)

        group = GroupConversation.objects.filter(pk=group_id)
        context = {
            'groupconversation': groupconversation,
            'groupconversationmembers': groupconversationmembers,
            'group': group
        }
        if request.method == 'POST' and not None:

            if 'content' in request.POST:
                content = request.POST['content']
            else:
                content = ''
            if 'image' in request.FILES is not None:
                image = request.FILES['image']
            else:
                image = ''

            message = GroupConversationMessage(groupconversation_id=group_id, content=content, image=image,
                                               created_by=request.user)
            if message.content != "" and message.image != "":
                print(message.image)
                y = imagepredict(message.image)
                if argmax(y) == 0 and float("{:.2f}".format((y[0][0] * 100))) > 85 or argmax(y) == 1 and float(
                        "{:.2f}".format((y[0][0] * 100))) > 85:
                    print("The model has predicted the image is MEME" +
                          ' with a Confidence of ' + "{:.2f}".format((y[0][0] * 100)) + '%')
                    messages.warning(request, 'Warning the image uploaded was classified as a prohibited Image')
                    return redirect('groupconversation', group_id)

                else:
                    print("good image")
                    if message.content == 'go':
                        message.content = 'GO TO BED'
                    message.save()
                    results = re.findall("(^|[^@\w])@(\w{1,20})", content)

                    for result in results:
                        result = result[1]

                        print(result)
                        # get user form database and do filtering
                        """if User.objects.filter(username=result).exists() and result != request.user.username:
                            # creating the notification if someone mentions you, or you mention them
                            create_notification(request, User.objects.get(username=result), 'mention')"""

                    return redirect('groupconversation', group_id)
            elif message.content == "" and message.image != "":
                print(message.image)
                y = imagepredict(message.image)
                if argmax(y) == 0 and float("{:.2f}".format((y[0][0] * 100))) > 85 or argmax(y) == 1 and float(
                        "{:.2f}".format((y[0][0] * 100))) > 85:
                    print("The model has predicted the image is MEME" +
                          ' with a Confidence of ' + "{:.2f}".format((y[0][0] * 100)) + '%')
                    messages.warning(request, ' Warning the image uploaded was classified as a prohibited Image')
                    return redirect('groupconversation', group_id)

                else:
                    print("good image")
                    message.save()
                    messages.success(request, 'Successfully Posted!!')
                    return redirect('groupconversation', group_id)

            elif message.content != "" and message.image is not None:

                if message.content == 'go':
                    message.content = 'GO TO BED'
                message.save()
                results = re.findall("(^|[^@\w])@(\w{1,20})", content)

                for result in results:
                    result = result[1]

                    print(result)
                    # get user form database and do filtering
                    """if User.objects.filter(username=result).exists() and result != request.user.username:
                        # creating the notification if someone mentions you, or you mention them
                        create_notification(request, User.objects.get(username=result), 'mention')"""
                messages.success(request, 'Successfully Posted!!')

                return redirect('groupconversation', group_id)
            else:
                return render(request, 'groupconversation/groupconversation.html', context)

        else:
            return render(request, 'groupconversation/groupconversation.html', context)
    else:
        return redirect('login')


@login_required
def listofgroupmembers(request, group_id):
    obj = GroupConversation.objects.get(id=group_id)
    if request.user.is_authenticated:
        groupconversationmembers = GroupConversationMembers.objects.filter(groupconversation=group_id)
        context = {
            'groupconversationmembers': groupconversationmembers,
            'obj':obj,
        }

        return render(request, 'groupconversation/group_members.html', context)
    else:
        return redirect('login')


@login_required
def deletegroupmessage(request, group_id, message_id):
    message = GroupConversationMessage.objects.get(id=message_id)  # we need this for both GET and POST
    context = {
        'message': message,
        'group_id': group_id,
    }
    if request.method == 'POST':
        # delete the feed from the database
        if request.user.studysocioprofile.user == message.created_by:
            message.delete()
            # redirect to the feed page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect('directconversation',user)

        # no need for an `else` here. If it's a GET request, just continue
    return render(request, 'groupconversation/groupconversation.html', context)

"""@login_required
def removegroupuser(request, group_id, user_id):
    user = GroupConversationMembers.objects.get(pk=user_id)  # we need this for both GET and POST
    context = {
        'user': user,
        'group_id': group_id,
    }
    if request.method == 'POST':
        # delete the feed from the database
        #if request.user.studysocioprofile.user == user:
        user.delete()
        # redirect to the feed page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect('directconversation',user)

        # no need for an `else` here. If it's a GET request, just continue
    return render(request, 'groupconversation/group_members.html', context)
"""
@login_required
def removegroupuser(request,group_id, user_id):
    user = GroupConversationMembers.objects.get(id=user_id)
    message =GroupConversationMessage.objects.filter(created_by=user_id,groupconversation=group_id)
    # we need this for both GET and POST
    groupconversationmembers = GroupConversationMembers.objects.filter(groupconversation=group_id)
    context = {
        'groupconversationmembers': groupconversationmembers
    }
    if request.method == 'POST':

        user.delete()
        message.delete()
        # redirect to the feed page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # no need for an `else` here. If it's a GET request, just continue

    return render(request, 'groupconversation/group_members.html', context)


@login_required
def deletegroup(request,group_id):
    groupconversations = GroupConversationMembers.objects.all()
    group = GroupConversation.objects.get(id=group_id)
    message =GroupConversationMessage.objects.filter(groupconversation=group_id)
    # we need this for both GET and POST
    groupconversationmembers = GroupConversationMembers.objects.filter(groupconversation=group_id)
    context = {
        'groupconversationmembers': groupconversationmembers,
        'groupconversations':groupconversations,
    }
    if request.method == 'POST':

        group.delete()
        message.delete()
        # redirect to the feed page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # no need for an `else` here. If it's a GET request, just continue

    return render(request, 'groupconversation/groupconversations.html', context)