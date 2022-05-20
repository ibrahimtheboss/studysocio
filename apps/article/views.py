from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
from apps.article.forms import ArticleForm
from apps.article.models import Article


def article(request):
    users = User.objects.all()
    if request.method =='POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = Article.objects.create(
                    user=User.objects.get(pk=request.user.id),
                    title=form.cleaned_data["title"],
                    titleimage=form.cleaned_data["titleimage"],
                    titleimagecaption=form.cleaned_data["titleimagecaption"],
                    category=form.cleaned_data["category"],
                    content=form.cleaned_data["content"]
            )
            article.save()
            return redirect('article')
    else:
        form = ArticleForm()

    context = {
        'form': form,
        "users": users
    }
    return render(request, 'article/article.html', context)


