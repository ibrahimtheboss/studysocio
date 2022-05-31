import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps.videolessons.models import Like, VideoLesson
from apps.notification.utilities import create_notification


@login_required
def api_like_lesson(request):
    data = json.loads(request.body)
    lesson_id = data['Lesson_id']

    if not Like.objects.filter(lesson_id= lesson_id).filter(created_by=request.user).exists():
        like = Like.objects.create(lesson_id= lesson_id, created_by=request.user)
        lesson = VideoLesson.objects.get(pk=lesson_id)
        create_notification(request, lesson.created_by,'like_lesson')

    return JsonResponse({'success': True})
