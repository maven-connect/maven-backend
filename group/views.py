from django.contrib.auth.decorators import login_required
from .models import Group, Message, PermissionIssueMessage
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.core import serializers
from django.http import JsonResponse
import json

# @login_required
# @require_POST
# def new_message(request, group_id):
#     group = get_object_or_404(Group, pk=group_id)

#     try:
#         user = request.user 
#         content = request.POST.get('content')
#         message = Message(group=group, user=user, content=content)
#         message.save()

#         chats = Message.objects.filter(group=group).order_by('timestamp')

#         chat_data = serializers.serialize('json', chats)

#         return JsonResponse({'chats': chat_data}, safe=False)
#     except:
#         return JsonResponse({'message': 'Error creating message'}, status=400)

@login_required
@require_POST
def new_group(request):
    try:
        user = request.user
        body = json.loads(request.body)
        group_name = body.get('name')
        group_batch = body.get('batch')
        group_branch = body.get('branch')
        description = body.get('description')

        if user.is_userStaff and group_name and group_batch:
            if group_branch:
                group = Group.objects.create(name=group_name, batch=group_batch, branch=group_branch, description=description, admin=user)
                group.users.add(user)
                return JsonResponse({"name":group.name, "batch": group.batch, "branch": group.branch, "description": group.description},status=200 )
            else:
                group = Group.objects.create(name=group_name, batch=group_batch, is_BatchCommon=True, description=description, admin=user)
                group.users.add(user)
                return JsonResponse({"name":group.name, "batch": group.batch, "branch": group.branch, "description": group.description},status=200 )
        else:
            return JsonResponse({'error': "No group name field found."}, status=400)
    except:
        return JsonResponse({"error": "Error"}, status=400)
    
@login_required
@require_GET
def get_joined_groups(request) :
    user = request.user    
    if user.is_verified:
        joined_groups = []
        for grp in user.group_set.all():
            joined_groups.append({"name":grp.name, "batch": grp.batch, "branch": grp.branch, "description": grp.description, "admin": grp.admin.email if grp.admin else None })
        return JsonResponse({"groups": joined_groups}, safe=False)
    else:
        return JsonResponse({'error': 'User is not verified.'}, status=400)
    
@login_required
@require_GET
def get_group_participants(request, group_name):
    user = request.user
    if user.is_verified:
        group = Group.objects.get(name=group_name)
        users = group.users.all()
        userList = []
        for item in users:
            userList.append({"email": item.email, "date_joined": item.date_joined, "branch": item.user_branch, "batch": item.batch})
        return JsonResponse({"userList": userList}, status=200)
    else:
        return JsonResponse({"error": "User not verified"})

@login_required
@require_GET
def get_group_data(request, group):
    user = request.user    
    if user.is_verified:
        group = get_object_or_404(Group, name=group)
        messages = Message.objects.filter(group=group).order_by('-timestamp')[:30]
        messages = messages[::-1]
        message_data = []
        for message in messages:
            message_data.append({
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'user': message.user.email,
                'groupName': message.group.name,
                'type': 'MSG',
            })
        
        permissionIssues = PermissionIssueMessage.objects.filter(group=group).order_by('-timestamp')[:30]
        permissionIssues = permissionIssues[::-1]
        isp_data = []
        for isp in permissionIssues:
            isp_data.append({
                'content': isp.content,
                'timestamp': isp.timestamp.isoformat(),
                'user': isp.user.email,
            	'groupName': isp.group.name,
                'type': 'ISP',
                'category': isp.category,
            })
        return JsonResponse({'messages': message_data, "isp": isp_data})
    else:
        return JsonResponse({'error': 'User is not verified.'}, status=400)