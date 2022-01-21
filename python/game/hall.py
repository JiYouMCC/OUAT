from .models import Cache
from account.views import get_user_by_id


class CacheKeys:
    HALL_USER_LIST = 'hall_user_list'
    HALL_PLAYER_LIST = 'hall_player_list'
    PLAYER_OWNER = 'player_owner'


# 确认登陆到了页面上socket连接的人，逻辑在consumers端
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

# 准备了参加游戏的用户
def get_players():
    result = Cache.get(CacheKeys.HALL_PLAYER_LIST)
    return result if result else []


def add_player(uid):
    add_user = get_user_by_id(uid)
    if add_user.is_authenticated:
        result = Cache.get(CacheKeys.HALL_PLAYER_LIST)
        flag = False
        if result:
            for user in result:
                if user['uid'] == add_user.id:
                    flag = True
        if flag:
            return result
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
            set_owner(add_user.id)
        Cache.set(CacheKeys.HALL_PLAYER_LIST, result)
        return result
    else:
        return None


def remove_player(uid):
    if uid:
        owner = get_owner()
        if owner.uid == uid:
            remove_owner()
        result = Cache.get(CacheKeys.HALL_PLAYER_LIST)
        result = [user for user in result if str(user['uid']) != str(uid)]
        Cache.set(CacheKeys.HALL_PLAYER_LIST, result)
        if len(result) > 0:
            set_owner(result[0].uid)
        return result
    else:
        return None

# 房主就是加入游戏的第一个人，没了就顺位，自动配置
def get_owner():
    result = Cache.get(CacheKeys.PLAYER_OWNER)
    return result if result else []


def remove_owner():
    Cache.set(CacheKeys.PLAYER_OWNER, None)


def set_owner(uid):
    owner = get_user_by_id(uid)
    Cache.set(CacheKeys.PLAYER_OWNER,
              {
              'username': owner.username,
               'uid': owner.id,
               'nickname': owner.last_name}
              )
    return get_owner()


# 游戏状态
class GameStatus:
    NOT_START = 'not start'
    PREPARING = 'preparing' # 有人报名未开始
    START = 'start' # 进行中

def get_game_status():
    pass

def set_game_status():
    pass

# 游戏阶段
class GameStage:
    TELL = 'tell' # 讲述中
    BREAK = 'break' # 中断中
    OBJECTION = 'objection'# 异议中
    SUMMARY = 'summary'# 总结中
    ENDING = 'ending' # 结局中

def get_game_stage():
    pass

def set_game_stage():
    pass


# 操作

def ouat_tell():
    pass

def ouat_break():
    pass

def ouat_objection():
    pass

def ouat_vote():
    pass

def ouat_summary():
    pass

def ouat_ending():
    pass