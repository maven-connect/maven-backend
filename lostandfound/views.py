from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.http.response import HttpResponse, JsonResponse
from .models import LostAndFoundModel


@login_required
@require_POST
def createLostFound(request):
    try:
        uploaded_image = request.FILES.get('image')
        name = request.POST.get('name')
        user = request.user
        if name:
            lost_and_found_item = LostAndFoundModel(
                name=name, image_url=uploaded_image)

            if request.POST.get('description'):
                lost_and_found_item.description = request.POST.get(
                    'description')

            lost_and_found_item.category = request.POST.get(
                'category')
            lost_and_found_item.save()
            lost_and_found_item.creator.add(user)

            return JsonResponse({'message': 'Item created successfully', 'image': lost_and_found_item.image_url})
        else:
            return JsonResponse({'message': 'Failed req'}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({'Message': 'Failed Req'}, status=400)


@login_required
@require_GET
def getLostFoundItems(request):
    try:
        LostItems = LostAndFoundModel.objects.filter(category="LOST").order_by(
            '-timestamp')[:30]
        LostItems = LostItems[::-1]

        FoundItems = LostAndFoundModel.objects.filter(category="FOUND").order_by(
            '-timestamp')[:30]
        FoundItems = FoundItems[::-1]

        LostData = []
        FoundData = []
        for i in LostItems:
            LostData.append(
                {'name': i.name, 'image': i.image_url.url, 'timestamp': i.timestamp})

        for i in FoundItems:
            FoundData.append(
                {'name': i.name, 'image': i.image_url.url, 'timestamp': i.timestamp})

        return JsonResponse({'LostData': LostData, 'FoundData': FoundData})
    except Exception as e:
        print(e)
        return JsonResponse({'Message': 'Failed Req'}, status=400)
