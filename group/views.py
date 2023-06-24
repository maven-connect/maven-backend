from django.contrib.auth.decorators import login_required
from .models import Group, Message
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import json

@login_required
@require_POST
def new_message(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    user = request.user 
    content = request.POST.get('content')
    message = Message(group=group, user=user, content=content)
    message.save()

    chats = Message.objects.filter(group=group).order_by('timestamp')

    chat_data = serializers.serialize('json', chats)

    return JsonResponse({'chats': chat_data}, safe=False)

@login_required
@require_POST
def new_group(request):
    user = request.user
    body = json.loads(request.body)
    group_name = body.get('name')
    group_batch = body.get('batch')
    if group_name and group_batch:
        group = Group.objects.create(name=group_name, batch=group_batch)
        group.users.add(user)
        return HttpResponse('Group %s created successfully.'%(group.name) )
    else:
        return HttpResponseBadRequest('No group name field found.')
    
@login_required
@require_GET
def get_joined_groups(request) :
    user = request.user    
    if user.is_verified:
        joined_groups = user.group_set.all()
        return JsonResponse(joined_groups, safe=False)
    else:
        return HttpResponseBadRequest('User is not verified.')

    