from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from apps.announcement.forms import AnnouncementForm
from apps.announcement.models import Announcement

@login_required
def announcements(request):
    announcement_list = Announcement.objects.all()
    context = {
        "announcement_list": announcement_list,
    }
    return render(request, 'announcement/announcements.html', context)

@login_required
def create_announcement(request):
    users = User.objects.all()
    if request.method =='POST':
        form = AnnouncementForm(request.POST, request.FILES)

        if form.is_valid():
            article = Announcement.objects.create(
                    created_by=User.objects.get(pk=request.user.id),
                    title=form.cleaned_data["title"],
                    Description=form.cleaned_data["Description"],
                    image=form.cleaned_data["image"],
                    video=form.cleaned_data["video"],
                    youtube_url=form.cleaned_data["youtube_url"],

            )
            messages.success(request, 'successfully Created Announcement')
            article.save()
            return redirect('create_announcement')
    else:
        form = AnnouncementForm()

    context = {
        'form': form,
        "users": users
    }
    return render(request, 'announcement/create_announcement.html', context)

@login_required
def delete_announcement(request,announcement_id,username):
    announcement_id_list = Announcement.objects.filter(created_by=request.user)
    announcement_ids_delete = Announcement.objects.get(id=announcement_id)
    context = {
        "announcement_id_list": announcement_id_list,
    }
    if request.method == 'POST':
        announcement_ids_delete.delete()
        messages.success(request, 'successfully Deleted Announcement.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'announcement/my_announcements.html', context)

@login_required
def my_announcements(request,username):
    announcement_list = Announcement.objects.filter(created_by=request.user)
    context = {
        "announcement_list": announcement_list,
    }
    return render(request, 'announcement/my_announcements.html', context)



@login_required
def edit_announcement(request,announcement_id,username):
    obj = Announcement.objects.get(id=announcement_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(request, 'successfully Saved Changes to Announcement.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = AnnouncementForm(instance=obj)

    context = {
        'obj': obj,
        'form': form
    }
    return render(request, "announcement/edit_announcement.html", context)