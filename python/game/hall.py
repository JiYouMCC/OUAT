from django.http import JsonResponse
from .models import Cache
from account.views import get_user_by_id

class CacheKeys:
    HALL_USER_LIST = 'hall_user_list'
    HALL_PLAYER_LIST = 'hall_player_list'


def get_users():
    result = Cache.get(CacheKeys.HALL_USER_LIST)
    return result if result else []


def add_user(uid):
    add_user = get_user_by_id(uid)
    if add_user.is_authenticated:
        result = Cache.get(CacheKeys.HALL_USER_LIST)
        result = [user for user in result if user['uid'] != add_user.id]
        if result:
            result.append(
                {
                    'username': add_user.username,
                    'uid': add_user.id,
                    'nickname': add_user.last_name,
                })
        else:
            result = [{
                'username': add_user.username,
                'uid': add_user.id,
                'nickname': add_user.last_name,
            }]
        Cache.set(CacheKeys.HALL_USER_LIST, result)
        return result
    else:
        return None


def remove_user(uid):
    if uid:
        result = Cache.get(CacheKeys.HALL_USER_LIST)
        result = [user for user in result if str(user['uid']) != str(uid)]
        Cache.set(CacheKeys.HALL_USER_LIST, result)
        return result
    else:
        return None


def get_players(request):
    result = Cache.get(CacheKeys.HALL_PLAYER_LIST)
    return JsonResponse({
        'result': True,
        'users': result if result else []
    })


def add_player(request):
    if request.user.is_authenticated:
        result = Cache.get(CacheKeys.HALL_PLAYER_LIST)
        flag = False
        for user in result:
            if user['uid'] == request.user.id:
                flag = True
        if flag:
            return JsonResponse({
                'result': True,
                'users': result
            })
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
                'admin': True
            }]
        Cache.set(CacheKeys.HALL_PLAYER_LIST, result)
        return JsonResponse({
            'result': True,
            'users': result
        })


def remove_player(request):
    uid = None
    if request.user.is_authenticated:
        uid = request.user.id
    else:
        uid = request.POST.get('uid', '')
    if uid:
        isAdmin = False
        for user in result:
            if user['uid'] == request.user.id:
                if user.admin:
                    isAdmin = True


        result = Cache.get(CacheKeys.HALL_PLAYER_LIST)
        result = [user for user in result if str(user['uid']) != str(uid)]
        Cache.set(CacheKeys.HALL_PLAYER_LIST, result)
        return JsonResponse({
            'result': True,
            'users': result
        })
    else:
        return JsonResponse({
            'result': False
        })
