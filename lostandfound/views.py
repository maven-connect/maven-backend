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

        if uploaded_image and name:
            lost_and_found_item = LostAndFoundModel(
                name=name, image_url=uploaded_image)

            if request.POST.get('description'):
                lost_and_found_item.description = request.POST.get(
                    'description')

            lost_and_found_item.category = request.POST.get(
                'category')
            lost_and_found_item.save()

            return JsonResponse({'message': 'Item created successfully'})
        else:
            return JsonResponse({'message': 'Failed req'}, status=400)

    except Exception as e:
        return HttpResponse('NONO')
