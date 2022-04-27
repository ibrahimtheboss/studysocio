import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import DirectConversationMessage


@login_required
def api_add_message(request):
    data = json.loads(request.body)
    content = data['content']
    conversation_id = data['conversation_id']
    image = data['image']

    message = DirectConversationMessage.objects.create(conversation_id=conversation_id, content=content, image=image,
                                                       created_by=request.user)

    return JsonResponse({'success': True})
