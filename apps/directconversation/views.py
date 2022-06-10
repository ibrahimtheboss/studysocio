import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from numpy import argmax

from apps.core.m_l_model import imagepredict
from apps.directconversation.models import DirectConversation, DirectConversationMessage
from apps.notification.utilities import create_notification

# Create your views here.



@login_required

def directconversations(request):

    directconversations = request.user.directconversations.all()
    directconversations = directconversations.filter(messages =F('messages')).distinct() # here we filter if coversation id  is in messages Fk coversatio nid
    return render(request, 'directconversation/directconversations.html', {'directconversations': directconversations})

@login_required
def directconversation(request, user_id):
    if request.user.is_authenticated:
        directconversations = DirectConversation.objects.filter(users__in=[request.user.id])
        directconversations = directconversations.filter(users__in=[user_id])  # other user id
        userss = User.objects.filter(id=user_id)

        if directconversations.count() == 1:
            directconversation = directconversations[0]  # first in the list

        else:
            recipient = User.objects.get(pk=user_id)
            directconversation = DirectConversation.objects.create()
            directconversation.users.add(request.user)  # logged in current user
            directconversation.users.add(recipient)
            directconversation.save()
        context = {
            'userss':userss,
            'directconversation': directconversation,
            'directconversations': directconversations,
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

            message = DirectConversationMessage(directconversation_id=directconversation.id, content=content, image=image,
                                                created_by=request.user)

            if message.content != "" and message.image != "":
                print(message.image)
                y = imagepredict(message.image)
                if argmax(y) == 0 and float("{:.2f}".format((y[0][0] * 100))) > 85:
                    print("The model has predicted the image is MEME" +
                          ' with a Confidence of ' + "{:.2f}".format((y[0][0] * 100)) + '%')
                    messages.warning(request, 'Warning the image uploaded was classified as a Meme image which is '
                                              'a prohibited Image')
                    return redirect('directconversation', user_id)
                elif argmax(y) == 1 and float("{:.2f}".format((y[0][1] * 100))) > 85:
                    print("The model has predicted the image is Selfie" +
                          ' with a Confidence of ' + "{:.2f}".format((y[0][1] * 100)) + '%')
                    messages.warning(request, 'Warning the image uploaded was classified as a Selfie image which is a '
                                              'prohibited Image')
                    return redirect('directconversation', user_id)


                else:
                    print("good image")
                    if message.content == 'go':
                        message.content = 'GO TO BED'
                    message.save()
                    results = re.findall("(^|[^@\w])@(\w{1,20})", content)

                    for result in results:
                        result = result[1]

                        print(result)
                    for user in message.directconversation.users.all():
                        if user != request.user:
                            create_notification(request, user, 'message')
                        # get user form database and do filtering
                        """if User.objects.filter(username=result).exists() and result != request.user.username:
                            # creating the notification if someone mentions you, or you mention them
                            create_notification(request, User.objects.get(username=result), 'mention')"""

                    return redirect('directconversation', user_id)
            elif message.content == "" and message.image != "":
                print(message.image)
                y = imagepredict(message.image)
                if argmax(y) == 0 and float("{:.2f}".format((y[0][0] * 100))) > 85:
                    print("The model has predicted the image is MEME" +
                          ' with a Confidence of ' + "{:.2f}".format((y[0][0] * 100)) + '%')
                    messages.warning(request, 'Warning the image uploaded was classified as a Meme image which is '
                                              'a prohibited Image')
                    return redirect('directconversation', user_id)
                elif argmax(y) == 1 and float("{:.2f}".format((y[0][1] * 100))) > 85:
                    print("The model has predicted the image is Selfie" +
                          ' with a Confidence of ' + "{:.2f}".format((y[0][1] * 100)) + '%')
                    messages.warning(request, 'Warning the image uploaded was classified as a Selfie image which is a '
                                              'prohibited Image')
                    return redirect('directconversation', user_id)

                else:
                    print("good image")
                    message.save()
                    messages.success(request, 'Successfully Posted!!')
                    return redirect('directconversation', user_id)

            elif message.content != "" and message.image is not None:

                if message.content == 'go':
                    message.content = 'GO TO BED'
                message.save()
                results = re.findall("(^|[^@\w])@(\w{1,20})", content)

                for result in results:
                    result = result[1]

                    print(result)
                for user in message.directconversation.users.all():
                    if user != request.user:
                        create_notification(request, user, 'message')
                    # get user form database and do filtering
                    """if User.objects.filter(username=result).exists() and result != request.user.username:
                        # creating the notification if someone mentions you, or you mention them
                        create_notification(request, User.objects.get(username=result), 'mention')"""
                messages.success(request, 'Successfully Posted!!')
            ###
                return redirect('directconversation', user_id)
            else:
                return render(request, 'directconversation/directconversation.html',
                              context)

        else:
            return render(request, 'directconversation/directconversation.html', context)

    return redirect('login')


@login_required
def deletemessage(request,user_id, message_id):


    message = DirectConversationMessage.objects.get(id=message_id)  # we need this for both GET and POST
    context = {
        'message': message,
        'user_id':user_id,
    }
    if request.method == 'POST':
        # delete the feed from the database
        if request.user.studysocioprofile.user == message.created_by:
            message.delete()
            # redirect to the feed page
            messages.success(request, 'Successfully Deleted Message !!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #return redirect('directconversation',user)

        # no need for an `else` here. If it's a GET request, just continue

    return render(request, 'directconversation/directconversation.html', context)

@login_required
def deletedirectconversations(request, user_id,directconversation_id):
    message = DirectConversationMessage.objects.all().filter(directconversation=directconversation_id)  # we need this for both GET and POST
    #deletemessage = DirectConversation.objects.filter(id= directconversation_id,users=request.user)  # we need this for both GET and POST
    context = {
        'message': message,
        'deletemessage':deletemessage,
        'user_id': user_id,
    }
    if request.method == 'POST':
        # delete the feed from the database
        if request.user.studysocioprofile.user == deletemessage:
            message.all().delete()
            # redirect to the feed page
            messages.success(request, 'Successfully Deleted Conversation !!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect('directconversation',user)

        # no need for an `else` here. If it's a GET request, just continue


    return render(request, 'directconversation/directconversations.html', context)
