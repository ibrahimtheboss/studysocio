import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps.article.models import Like, Article
from apps.notification.utilities import create_notification


@login_required
def api_like_article(request):
    data = json.loads(request.body)
    articles_id = data['Article_id']

    if not Like.objects.filter(Article_id= articles_id).filter(created_by=request.user).exists():
        like = Like.objects.create(Article_id= articles_id, created_by=request.user)
        article = Article.objects.get(pk=articles_id)
        create_notification(request, article.created_by,'like_article',articles_id)

    return JsonResponse({'success': True})
