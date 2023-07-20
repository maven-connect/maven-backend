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

    try:
        user = request.user 
        content = request.POST.get('content')
        message = Message(group=group, user=user, content=content)
        message.save()

        chats = Message.objects.filter(group=group).order_by('timestamp')

        chat_data = serializers.serialize('json', chats)

        return JsonResponse({'chats': chat_data}, safe=False)
    except:
        return JsonResponse({'message': 'Error creating message'}, status=400)

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
        return JsonResponse({'message': 'Group %s created successfully.'%(group.name)},status=200 )
    else:
        return HttpResponseBadRequest('No group name field found.')
    
@login_required
@require_GET
def get_joined_groups(request) :
    user = request.user    
    if user.is_verified:
        joined_groups = []
        for grp in user.group_set.all():
            joined_groups.append({"name":grp.name, "batch": grp.batch})
        return JsonResponse({"groups": joined_groups}, safe=False)
    else:
        return JsonResponse({'error': 'User is not verified.'}, status=400)
    

@login_required
@require_GET
def get_group_messages(request, group):
    user = request.user    
    if user.is_verified:
        group = get_object_or_404(Group, name=group)
        messages = Message.objects.filter(group=group).order_by('timestamp')[:30]

        message_data = []
        for message in messages:
            message_data.append({
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'user': message.user.email,
            })
        
        return JsonResponse({'messages': message_data})
    else:
        return JsonResponse({'error': 'User is not verified.'}, status=400)