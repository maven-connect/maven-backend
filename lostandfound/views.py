from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.http.response import HttpResponse, JsonResponse
from .models import LostAndFoundModel
import json


@login_required
@require_POST
def createLostFound(request):
    try:
        uploaded_image = request.FILES.get('image')
        name = request.POST.get('name')
        user = request.user
        if name:
            lost_and_found_item = LostAndFoundModel(
                name=name, image_url=uploaded_image, user=user)

            if request.POST.get('description'):
                lost_and_found_item.description = request.POST.get(
                    'description')

            lost_and_found_item.category = request.POST.get(
                'category')
            lost_and_found_item.save()

            return JsonResponse({'name': lost_and_found_item.name, 'id': lost_and_found_item.pk, 'description': lost_and_found_item.description if lost_and_found_item.description else None, 'image': lost_and_found_item.image_url.url if lost_and_found_item.image_url else None, 'timestamp': lost_and_found_item.timestamp, 'user': lost_and_found_item.user.email, 'contacts': []})
        else:
            return JsonResponse({'message': 's req'}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({'Message': 'Failed Req'}, status=400)


@login_required
@require_GET
def getLostFoundItems(request):
    try:
        LostItems = LostAndFoundModel.objects.filter(category="LOST").order_by(
            '-timestamp')[:30]

        FoundItems = LostAndFoundModel.objects.filter(category="FOUND").order_by(
            '-timestamp')[:30]

        LostData = []
        FoundData = []
        for i in LostItems:
            contactList = []
            for cont in i.contacts.all():
                contactList.append(
                    {'email': cont.email, 'batch': cont.batch, 'branch': cont.user_branch})
            LostData.append(
                {'name': i.name, 'id': i.pk, 'description': i.description if i.description else None, 'image': i.image_url.url if i.image_url else None, 'timestamp': i.timestamp, 'user': i.user.email, 'contacts': contactList})

        for i in FoundItems:
            contactList = []
            for cont in i.contacts.all():
                contactList.append(
                    {'email': cont.email, 'batch': cont.batch, 'branch': cont.user_branch})
            FoundData.append(
                {'name': i.name, 'id': i.pk, 'description': i.description if i.description else None, 'image': i.image_url.url if i.image_url else None, 'timestamp': i.timestamp, 'user': i.user.email, 'contacts': contactList})

        return JsonResponse({'LostData': LostData, 'FoundData': FoundData})
    except Exception as e:
        print(e)
        return JsonResponse({'Message': 'Failed Req'}, status=400)


@login_required
@require_http_methods(["DELETE"])
def deleteLostFoundItem(request):
    try:
        body = json.loads(request.body)
        id = body.get('id')
        lostFoundItem = LostAndFoundModel.objects.get(pk=id)
        if lostFoundItem.user.email == request.user.email:
            lostFoundItem.delete()
            return JsonResponse({'message': 'Successfully Deleted'})
        else:
            return JsonResponse({'message': "Unauthorized"}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Failed Req'}, status=400)


@login_required
@require_POST
def addContacts(request):
    body = json.loads(request.body)
    id = body.get('id')
    lostFoundItem = LostAndFoundModel.objects.get(pk=id)
    try:
        if request.user not in lostFoundItem.contacts.all():
            lostFoundItem.contacts.add(request.user)
            lostFoundItem.save()
        contactList = []
        for cont in lostFoundItem.contacts.all():
            contactList.append(
                {'email': cont.email, 'batch': cont.batch, 'branch': cont.user_branch})
        return JsonResponse({'name': lostFoundItem.name, 'id': lostFoundItem.pk, 'description': lostFoundItem.description if lostFoundItem.description else None, 'image': lostFoundItem.image_url.url if lostFoundItem.image_url else None, 'timestamp': lostFoundItem.timestamp, 'user': lostFoundItem.user.email, 'contacts': contactList})
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Failed Req'}, status=400)
