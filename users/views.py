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


def home(request):
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
        idinfo = id_token.verify_oauth2_token(
            idToken, requests.Request(), CLIENT_ID)
        email = idinfo.get('email')
        user = authenticate(request, email=email)
        if user is not None:
            login(request, user, backend='server.authBackend.CustomAuth')
            return JsonResponse({'email': email, 'verified': user.is_verified}, status=200)
        else:
            user = CustomUser.objects.create_user(email=email)
            login(request, user, backend='server.authBackend.CustomAuth')
            return JsonResponse({'email': email, 'verified': user.is_verified}, status=200)
    except ValueError as e:
        return JsonResponse({'error': '%s' % e}, status=400)


@require_POST
def login_view(request):
    try:
        body = json.loads(request.body)
        email = body.get('email')
        password = body.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user, backend='server.authBackend.CustomAuth')
            return JsonResponse({'email': user.email, 'verified': user.is_verified, "is_staff": user.is_userStaff}, status=200)
        else:
            return JsonResponse({'error': 'Invalid email or password.'}, status=400)
    except:
        return JsonResponse({"message": "Bad Request"}, status=400)


@require_POST
def register_user(request):
    try:
        body = json.loads(request.body)
        email = body.get('email')
        password = body.get('password')
        if email.endswith('@iiitdmj.ac.in'):
            user_exists = CustomUser.objects.filter(email=email).exists()

            if user_exists or request.user.is_authenticated:
                return HttpResponseBadRequest('User already exists')
            else:
                user = CustomUser.objects.create_user(
                    email=email, password=password)
                return JsonResponse({'message': 'Successfully Registered'})
        else:
            return HttpResponseBadRequest('Only IIITDMJ organisation emails can be registered.')
    except:
        return JsonResponse({"message": "Bad Request"}, status=400)


@require_POST
@login_required
def verify_user(request):
    user = CustomUser.objects.get(email=request.user.email)
    body = json.loads(request.body)
    branch = body.get('branch')
    batch = body.get('batch')
    if branch and batch:
        try:
            user.batch = int(batch)
            user.user_branch = branch
            user.is_verified = True
            batch_groups = Group.objects.filter(
                batch=batch, is_BatchCommon=True)
            for group in batch_groups:
                group.users.add(user)

            branch_groups = Group.objects.filter(batch=batch, branch=branch)
            for group in branch_groups:
                group.users.add(user)

            user.save()
            return JsonResponse({'message': 'Verification successfull'})
        except KeyError as e:
            print(e)
            return JsonResponse({'error': 'Incorrect Payload'}, status=400)


def logout_view(request):
    logout(request)
    return HttpResponse('Logged out')


@require_GET
def get_profile(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse({'message': 'User is authenticated', 'email': user.email, 'verified': user.is_verified, 'is_userStaff': user.is_userStaff, 'branch': user.user_branch})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status='403')
