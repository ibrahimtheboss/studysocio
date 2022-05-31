from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from apps.topic.models import Topic
from apps.videolessons.forms import VideoLessonForm
from apps.videolessons.models import VideoLesson, Like

@login_required
def create_lesson(request):
    if request.user.studysocioprofile.designation == "Teacher":
        users = User.objects.all()
        if request.method =='POST':
            form = VideoLessonForm(request.POST, request.FILES)
            if form.is_valid():
                article = VideoLesson.objects.create(
                        created_by=User.objects.get(pk=request.user.id),
                        title=form.cleaned_data["title"],
                        Description=form.cleaned_data["Description"],
                        image=form.cleaned_data["image"],
                        youtube_url=form.cleaned_data["youtube_url"],
                        category=form.cleaned_data["category"],
                        status=form.cleaned_data["status"],

                )
                messages.success(request, 'successfully Created Lesson ')
                article.save()
                return redirect('create_lesson')
        else:
            form = VideoLessonForm()

        context = {
            'form': form,
            "users": users
        }
        return render(request, 'videolessons/create_lesson.html', context)
    else:
        return redirect('lessons_category')

@login_required
def lessons_category(request):
    categorys = Topic.objects.all()


    context = {
        "categorys": categorys
    }
    return render(request, 'videolessons/lessons_category.html', context)

@login_required
def lessons(request,category_id):
    query = request.GET.get('query', '')
    if len(query) > 0:
        lessons = VideoLesson.objects.filter(title__icontains=query, category=category_id)
    else:
        lessons = []
    lessons_list = VideoLesson.objects.filter(category=category_id,status="Publish")
    lessons_Category = Topic.objects.get(id=category_id)
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
        'lessons_Category':lessons_Category,
        'page_obj':page_obj,
        'lessons':lessons,
    }
    return render(request, 'videolessons/lessons.html', context)

@login_required
def per_lesson(request,category_id,lesson_id):
    lessons = VideoLesson.objects.get(id=lesson_id)
    userids = [request.user.id]

    Likes = Like.objects.filter(lesson=lesson_id)


    context = {
        "lessons": lessons,
        'Likes':Likes,
    }
    return render(request, 'videolessons/per_lesson.html', context)

@login_required
def your_lessons(request,username):
    if request.user.studysocioprofile.designation == "Teacher" and request.user.username == username:
        lessons_list = VideoLesson.objects.filter(created_by=request.user)
        context = {
            "lessons_list": lessons_list,
        }
        return render(request, 'videolessons/your_lessons.html', context)
    else:
        return redirect('lessons_category')

@login_required
def delete_lesson(request,lesson_id,username):
    if request.user.studysocioprofile.designation == "Teacher" and request.user.username == username:
        lessons_list = VideoLesson.objects.filter(created_by=request.user)
        lessons_delete = VideoLesson.objects.get(id=lesson_id)
        context = {
            "lessons_list": lessons_list,
        }
        if request.method == 'POST':
            lessons_delete.delete()
            messages.success(request, 'successfully Deleted lesson.')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'videolessons/your_lessons.html', context)
    else:
        return redirect('lessons_category')

@login_required
def my_per_lesson(request,lesson_id,username):
    if request.user.studysocioprofile.designation == "Teacher" and request.user.username == username:
        lessons = VideoLesson.objects.get(id=lesson_id)

        Likes = Like.objects.filter(lesson=lesson_id)


        context = {
            "lessons": lessons,
            'Likes':Likes,
        }
        return render(request, 'videolessons/my_lesson_view.html', context)
    else:
        return redirect('lessons_category')

@login_required
def edit_lesson(request,lesson_id,username):
    if request.user.studysocioprofile.designation == "Teacher" and request.user.username == username:
        obj = VideoLesson.objects.get(id=lesson_id)
        if request.method == 'POST':
            form = VideoLessonForm(request.POST, request.FILES, instance=obj)

            if form.is_valid():
                form.save()
                messages.success(request, 'successfully Saved Changes to Lesson.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = VideoLessonForm(instance=obj)

        context = {
            'obj': obj,
            'form': form
        }
        return render(request, "videolessons/edit_lesson.html", context)
    else:
        return redirect('lessons_category')
