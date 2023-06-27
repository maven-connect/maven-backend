from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from google.auth.transport import requests
from google.oauth2 import id_token
import json
from django.contrib.auth import authenticate, login, logout
import os
from django.contrib.auth import get_user_model
from group.models import Group

CustomUser = get_user_model()

CLIENT_ID = os.getenv('APP_CLIENT_ID')

def home(request) :
    return HttpResponse('Maven Backend Server')

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
            login(request, user, backend='server.authBackend.CustomAuth')
            return JsonResponse({'email': email, 'verified': user.is_verified}, status=200)
        else:
            user = CustomUser(email=email)
            user.set_unusable_password()
            user.save()
            login(request, user, backend='server.authBackend.CustomAuth')
            return JsonResponse({'email': email, 'verified': user.is_verified}, status=200)
    except ValueError as e:
        return HttpResponseBadRequest('Bad request:  %s' %e)
    
@require_POST
def login_view(request):
    body = json.loads(request.body)
    email = body.get('email')
    password = body.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user, backend='server.authBackend.CustomAuth')
        return JsonResponse({'email': user.email, 'verified': user.is_verified}, status=200)
    else:
        return HttpResponseBadRequest('Invalid email or password.')
    
@require_POST
def register_user(request):
    body = json.loads(request.body)
    email = body.get('email')
    password = body.get('password')
    if email.endswith('@iiitdmj.ac.in'):
        user_exists = CustomUser.objects.filter(email=email).exists()

        if user_exists or request.user.is_authenticated:
            return HttpResponseBadRequest('User already exists')
        else:
            user = CustomUser.objects.create_user(email=email,password=password)
            return JsonResponse({'message': 'Successfully Registered'})
    else:
        return HttpResponseBadRequest('Only IIITDMJ organisation emails can be registered.')

@require_POST
@login_required
def verify_user(request):
    user = CustomUser.objects.get(email=request.user.email)
    body = json.loads(request.body)
    branch = body.get('branch')
    batch = body.get('batch')
    if branch and batch :
        try:
            user.batch = int(batch)
            user.branch = branch
            user.is_verified = True
            user.save()
            matching_groups = Group.objects.filter(batch=batch, branch=branch)
            for group in matching_groups:
                group.users.add(user)
            return JsonResponse({'message': 'Verification successfull'})
        except:
            return HttpResponseBadRequest('Incorrect Payload')

def logout_view(request):
    logout(request)
    return HttpResponse('Successfully Logged out.')

@require_GET
def get_profile(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'User is authenticated', 'email': request.user.email, 'verified': request.user.is_verified})
    else:
        return JsonResponse({'error': 'User not authenticated'},status='403')
    
