from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from apps.groupconversation.forms import GroupConversationForm, GroupConversationMembersForm
from apps.groupconversation.models import GroupConversation, GroupConversationMembers


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
            #groupconversation.users.set(user)


            return redirect('create_group')
    else:
        form = GroupConversationForm()
        return render(request, "groupconversation/groupconversation.html", {'form': form})

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