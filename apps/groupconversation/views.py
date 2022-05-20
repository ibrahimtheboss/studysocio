import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from apps.directconversation.models import DirectConversationMessage
from apps.groupconversation.forms import GroupConversationForm, GroupConversationMembersForm
from apps.groupconversation.models import GroupConversation, GroupConversationMembers, GroupConversationMessage


def create_group(request):

    if request.method == 'POST':
        form = GroupConversationForm(request.POST, request.FILES)
        if form.is_valid():
            groupconversation = GroupConversation.objects.create(

                created_by=User.objects.get(pk=request.user.id),
                name=form.cleaned_data["name"],
                groupimage=form.cleaned_data["groupimage"],
                 )


            #user_id = request.POST.get('users')
            #user = User.objects.get(id=user_id)
            groupconversation.save()
            #GroupConversationMembers.objects.create(users=request.user,groupconversation=request.groupconversation__set.id)


            #groupconversation.users.set(user)


            return redirect('create_group')
    else:
        form = GroupConversationForm()
        return render(request, "groupconversation/create_group.html", {'form': form})

def add_member(request):

    if request.method == 'POST':
        form = GroupConversationMembersForm(request.POST, request.FILES)
        form.fields['groupconversation'].queryset = GroupConversation.objects.filter(created_by=request.user.id)
        if form.is_valid():
            groupconversationmembers = GroupConversationMembers.objects.create(
                users=form.cleaned_data["users"],
                groupconversation=form.cleaned_data["groupconversation"],
                 )
            #if not GroupConversationMembers.objects.filter(users=groupconversationmembers.users,groupconversation =groupconversationmembers.groupconversation).exists():
            #user_id = request.POST.get('users')
            #user = User.objects.get(id=user_id)
            groupconversationmembers.save()
            #groupconversation.users.set(user)


            return redirect('add_members')
        else:
            return render(request, "groupconversation/add_members.html",
                          {'form': form})
    else:
        form = GroupConversationMembersForm(user=request.user)
        return render(request, "groupconversation/add_members.html", {'form': form})



@login_required
def groupconversations(request):

    groupconversations = GroupConversationMembers.objects.all()
    #groupconversations = groupconversations.filter(messages =F('messages')).distinct() # here we filter if coversation id  is in messages Fk coversatio nid

    return render(request, 'groupconversation/groupconversations.html', {'groupconversations': groupconversations})


@login_required
def groupconversation(request, group_id):
    try:
        groupmembers = GroupConversationMembers.objects.get(groupconversation=group_id, users=request.user)
    except GroupConversationMembers.DoesNotExist:
        raise Http404("Post not found")
    if request.user.is_authenticated and groupmembers:
        groupconversation = GroupConversationMessage.objects.all()
        groupconversationmembers = GroupConversationMembers.objects.filter(groupconversation=group_id)


        group = GroupConversation.objects.filter(pk=group_id)
        context = {
            'groupconversation': groupconversation,
            'groupconversationmembers':groupconversationmembers,
            'group':group
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
            if message.content != "" and message.image is not None:
                if message.content == 'go':
                    message.content = 'GO TO BED'
                message.save()
                results = re.findall("(^|[^@\w])@(\w{1,20})", content)

                for result in results:
                    result = result[1]

                    print(result)




                return redirect('groupconversation', group_id)
            else:
                return render(request, 'groupconversation/groupconversation.html',context)

        else:
            return render(request, 'groupconversation/groupconversation.html', context)
    else:
        return redirect('login')

@login_required
def listofgroupmembers(request, group_id):
    if request.user.is_authenticated:
        groupconversationmembers = GroupConversationMembers.objects.filter(groupconversation=group_id)
        context = {
            'groupconversationmembers':groupconversationmembers
        }


        return render(request, 'groupconversation/group_members.html', context)
    else:
        return redirect('login')

@login_required
def deletegroupmessage(request,group_id, message_id):


    message = GroupConversationMessage.objects.get(id=message_id)  # we need this for both GET and POST
    context = {
        'message': message,
        'group_id':group_id,
    }
    if request.method == 'POST':
        # delete the feed from the database
        if request.user.studysocioprofile.user == message.created_by:
            message.delete()
            # redirect to the feed page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #return redirect('directconversation',user)

        # no need for an `else` here. If it's a GET request, just continue
    return render(request, 'groupconversation/groupconversation.html', context)
