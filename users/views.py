from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from google.auth.transport import requests
from google.oauth2 import id_token
import json
from django.contrib.auth import authenticate, login, logout
import os
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

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
            return JsonResponse({'email': email, 'verified': user.is_verified}, status=200)
        else:
            user = CustomUser(username=email,email=email)
            user.set_unusable_password()
            user.save()
            login(request, user)
            return JsonResponse({'email': email, 'verified': user.is_verified}, status=200)
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
        return JsonResponse({'email': user.email, 'verified': user.is_verified}, status=200)
    else:
        return HttpResponseBadRequest('Invalid username or password.')
    
@require_POST
def register_user(request):
    body = json.loads(request.body)
    username = body.get('email')
    password = body.get('password')
    user_exists = CustomUser.objects.filter(username=username).exists()

    if user_exists or request.user:
        return HttpResponseBadRequest('User already exists')
    else:
        user = CustomUser(username=username,password=password)
        user.save()
        return HttpResponse('Successfully Registered')

@require_POST
def verify_user(request):
    if request.user.is_authenticated:
        pass
    else:
        return HttpResponseBadRequest('Authenticate User')

def logout_view(request):
    logout(request)
    return HttpResponse('Successfully Logged out.')

