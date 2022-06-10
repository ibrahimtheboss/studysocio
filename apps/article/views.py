from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
from apps.article.forms import ArticleForm
from apps.article.models import Article, Category,Like
from apps.classroom.models import Classroom
from apps.topic.models import Topic

@login_required
def create_article(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        if request.method =='POST':
            form = ArticleForm(request.POST, request.FILES)

            if form.is_valid():
                article = Article.objects.create(
                        created_by=User.objects.get(pk=request.user.id),
                        title=form.cleaned_data["title"],
                        description=form.cleaned_data["description"],
                        titleimage=form.cleaned_data["titleimage"],
                        titleimagecaption=form.cleaned_data["titleimagecaption"],
                        category=form.cleaned_data["category"],
                        content=form.cleaned_data["content"],
                        status=form.cleaned_data["status"],

                )
                messages.success(request, 'successfully Created Article')
                article.save()
                return redirect('create_article')
        else:
            form = ArticleForm()

        context = {
            'form': form,
            "users": users
        }
        return render(request, 'article/article.html', context)
    else:
        return redirect('article_category')
@login_required
def article_category(request):
    categorys = Topic.objects.all()


    context = {
        "categorys": categorys
    }
    return render(request, 'article/article_category.html', context)


@login_required
def articles(request,category_id):
    query = request.GET.get('query', '')
    if len(query) > 0:
        articles = Article.objects.filter(title__icontains=query,category=category_id)
    else:
        articles = []

    articles_list = Article.objects.filter(category=category_id,status="Publish")
    articles_Category = Topic.objects.get(id=category_id)
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
        'articles_Category':articles_Category,
        'page_obj': page_obj,
        "articles":articles,
        'query':query,
    }
    return render(request, 'article/articles.html', context)
@login_required
def per_article(request,category_id,article_id):
    articles = Article.objects.get(id=article_id)
    userids = [request.user.id]

    Likes = Like.objects.filter(Article=article_id)


    context = {
        "articles": articles,
        'Likes':Likes,
    }
    return render(request, 'article/per_article.html', context)
@login_required
def your_articles(request,user_name):
    if request.user.is_authenticated and request.user.username ==user_name :
        articles_list = Article.objects.filter(created_by=request.user)
        context = {
            "articles_list": articles_list,
        }
        return render(request, 'article/your_articles.html', context)
    else:
        return redirect('article_category')

@login_required
def delete_articles(request,article_id,user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        articles_list = Article.objects.filter(created_by=request.user)
        articles_delete = Article.objects.get(id=article_id)
        context = {
            "articles_list": articles_list,
        }
        if request.method == 'POST':
            articles_delete.delete()
            messages.success(request, 'successfully Deleted Article.')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'article/your_articles.html', context)
    else:
        return redirect('article_category')
@login_required
def my_per_article(request,article_id,user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        articles = Article.objects.get(id=article_id)

        Likes = Like.objects.filter(Article=article_id)


        context = {
            "articles": articles,
            'Likes':Likes,
        }
        return render(request, 'article/per_article.html', context)
    else:
        return redirect('article_category')

@login_required
def edit_article(request,article_id,user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        obj = Article.objects.get(id=article_id)
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=obj)

            if form.is_valid():
                form.save()
                messages.success(request, 'successfully Saved Changes to Article.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = ArticleForm(instance=obj)

        context = {
            'obj': obj,
            'form': form
        }
        return render(request, "article/article.html", context)
    else:
        return redirect('article_category')






