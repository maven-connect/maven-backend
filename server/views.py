from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from urllib import parse
from google.auth.transport import requests
from google.oauth2 import id_token
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import os

CLIENT_ID = os.getenv('APP_CLIENT_ID')

@csrf_exempt
@require_POST
def googleLogin(request):
    # body_unicode = request.body.decode('utf-8')
    # body_params = parse.parse_qs(body_unicode)
    # csrf_token_cookie = request.COOKIES.get('g_csrf_token')
    # if not csrf_token_cookie:
    #     return HttpResponseBadRequest('No CSRF token in Cookie.')
    # csrf_token_body = body_params.get('g_csrf_token')
    # if not csrf_token_body:
    #     return HttpResponseBadRequest('No CSRF token in post body.')
    # if csrf_token_cookie != csrf_token_body[0]:
    #     return HttpResponseBadRequest('Failed to verify double submit cookie.')
    try:
        idToken = json.loads(request.body).get('id_token')
        idinfo = id_token.verify_oauth2_token(idToken, requests.Request(), CLIENT_ID)

        email = idinfo.get('email')
        user = authenticate(request, email=email)
        if user is not None:
            login(request, user)
            return JsonResponse({'email': email})
        else:
            user = User(username=email)
            user.set_unusable_password()
            user.save()
            login(request, user)
            return JsonResponse({'email': email})
    except ValueError as e:
        return HttpResponseBadRequest('Bad request')
    
@require_POST
def login_view(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'email': user.email})
    else:
        return JsonResponse({'error': 'Invalid username or password'}, status=401)

def logout_view(request):
    logout(request)
    return HttpResponse('Successfully Logged out.')

