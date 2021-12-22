from .models import Token
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
import uuid


def create_token(user):
    clear_token(user)
    token = Token(user=user, token=uuid.uuid4().hex)
    token.save()
    return token.token


def clear_token(user):
    Token.objects.filter(user=user).delete()


def get_user_by_token(token):
    token = Token.objects.filter(token=token)[0]
    if token:
        return token.user
    else:
        return None

def get_user_by_id(uid):
    user = User.objects.filter(id=uid)[0]
    if user:
        return user
    else:
        return None


def get_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'result': True,
            'nickname': request.user.last_name,
            'token': create_token(request.user)
        })
    else:
        return JsonResponse({
            'result': False
        })


def login(request):
    if request.user.is_authenticated:
        logout(request)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return JsonResponse({
            'result': True,
            'nickname': user.last_name,
            'token': create_token(request.user)
        })
    else:
        return JsonResponse({
            'result': False
        })


def logout(request):
    if request.user.is_authenticated:
        user = request.user
        clear_token(user)
        auth.logout(request)
        return JsonResponse({
            'result': True,
            'uid': user.id
        })
    else:
        return JsonResponse({
            'result': False
        })


def register(request):
    if request.user.is_authenticated:
        logout(request)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    nickname = request.POST.get('nickname', '')
    try:
        user = User.objects.create_user(username=username, password=password)
        user = auth.authenticate(username=username, password=password)
        user.last_name = nickname
        user.save()
        auth.login(request, user)
    except Exception as e:
        return JsonResponse({'result': False, 'message': str(e)})
    return JsonResponse({
        'result': True,
        'nickname': nickname,
        'token': create_token(user)})


def change_nickname(request):
    if request.user.is_authenticated:
        nickname = request.POST.get('nickname', '')
        user = request.user
        user.last_name = nickname
        user.save()
        return JsonResponse({'result': True, 'nickname': nickname})
    else:
        return JsonResponse({'result': False})
