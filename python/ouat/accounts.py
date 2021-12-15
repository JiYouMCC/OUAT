from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.models import User


def login(request):
    if request.user.is_authenticated:
        return JsonResponse({'result': True, 'nickname': request.user.last_name})
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return JsonResponse({'result': True, 'nickname':user.last_name})
    else:
        return JsonResponse({'result': False,'user':user})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return JsonResponse({'result': True})


def register(request):
    if request.user.is_authenticated:
        return JsonResponse({'result': False, 'message': 'Already login'})
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('username', '')
    nickname = request.POST.get('nickname', '')
    try:
        user = User.objects.create_user(username,email,password)
        user = auth.authenticate(username=username, password=password)
        user.last_name = nickname
        user.save()
        auth.login(request, user)
    except Exception as e:
        return JsonResponse({'result': False, 'message': str(e)})
    return JsonResponse({'result': True})

def change_nickname(request):
    if request.user.is_authenticated:
        nickname = request.POST.get('nickname', '')
        user = request.user
        user.last_name = nickname
        user.save()
        return JsonResponse({'result': True, 'nickname': nickname})
    else:
        return JsonResponse({'result': False})