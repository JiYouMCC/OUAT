from django.contrib.auth.decorators import login_required
from django.core.cache import caches
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import Cache


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def get_users(request):
    result = Cache.get('hall_user_list')
    return JsonResponse({
        'result': True,
        'users': result if result else []
    })


def add_user(request):
    if request.user.is_authenticated:
        result = Cache.get('hall_user_list')
        result = [user for user in result if user['uid'] != request.user.id]
        if result:
            result.append(
                {
                    'username': request.user.username,
                    'uid': request.user.id,
                    'nickname': request.user.last_name,
                })
        else:
            result = [{
                'username': request.user.username,
                'uid': request.user.id,
                'nickname': request.user.last_name,
            }]
        Cache.set('hall_user_list', result)
        return JsonResponse({
            'result': True,
            'users': result
        })
    else:
        return JsonResponse({
            'result': False
        })

def remove_user(request):
    uid = None
    if request.user.is_authenticated:
        uid = request.user.id
    else:
        uid = request.POST.get('uid', '')
    if uid:
        result = Cache.get('hall_user_list')
        result = [user for user in result if str(user['uid']) != str(uid)]
        Cache.set('hall_user_list', result)
        return JsonResponse({
            'result': True,
            'users': result
        })
    else:
        return JsonResponse({
            'result': False
        })

def get_players(request):
    result = Cache.get('hall_players_list')
    return JsonResponse({
        'result': True,
        'users': result if result else []
    })

def add_player(request):
    if request.user.is_authenticated:
        result = Cache.get('hall_player_list')
        result = [user for user in result if user['uid'] != request.user.id]
        if result:
            result.append(
                {
                    'username': request.user.username,
                    'uid': request.user.id,
                    'nickname': request.user.last_name,
                })
        else:
            result = [{
                'username': request.user.username,
                'uid': request.user.id,
                'nickname': request.user.last_name,
            }]
        Cache.set('hall_user_list', result)
        return JsonResponse({
            'result': True,
            'users': result
        })
