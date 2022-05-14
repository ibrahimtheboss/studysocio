import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


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
    directconversations = DirectConversation.objects.filter(users__in=[request.user.id])
    directconversations = directconversations.filter(users__in=[user_id])  # other user id

    if directconversations.count() == 1:
        directconversation = directconversations[0]  # first in the list

    else:
        recipient = User.objects.get(pk=user_id)
        directconversation = DirectConversation.objects.create()
        directconversation.users.add(request.user)  # logged in current user
        directconversation.users.add(recipient)
        directconversation.save()

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
        if message.content != "" and message.image is not None:
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


            return redirect('directconversation', user_id)
        else:
            return render(request, 'directconversation/directconversation.html',
                          {'directconversation': directconversation})

    else:
        return render(request, 'directconversation/directconversation.html', {'directconversation': directconversation})

    return render(request, 'directconversation/directconversation.html', {'directconversation': directconversation})


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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect('directconversation',user)

        # no need for an `else` here. If it's a GET request, just continue


    return render(request, 'directconversation/directconversations.html', context)
