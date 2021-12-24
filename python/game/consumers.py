from .models import Message, Cache
from account.views import get_user_by_id
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
import json
from .hall import add_user, remove_user, get_users, get_players, get_owner, add_player
import logging


class SystemMessageText:
    USER_LIST = 'user_list'  # 隐藏
    ONLINE = 'online'  # 用户活跃
    OFFLINE = 'offline'  # 用户不活跃


class MessageType:
    SYSTEM = 'system'  # 系统消息
    CHAT = 'chat'  # 聊天消息
    GAME = 'game'  # 游戏消息


class GameMessageCommand:
    ATTEND = 'attend'  # 加入游戏
    CANCEL = 'cancel'  # 取消加入
    QUIT = 'quit'  # 游戏中退出
    BREAK = 'break'  # 中断
    TELL = 'tell'  # 讲述
    SUMMARIZE = 'summa'  # 结束三段论
    FINAL = 'final'  # 讲述结局


def get_online_message(user, datetime):
    return {
        'text': SystemMessageText.ONLINE,
        'datetime': datetime.strftime("%Y-%m-%d %H:%M:%S%z"),
        'sender': {
            'uid': user.id,
            'nickname': user.last_name
        },
        'type': MessageType.SYSTEM,
        'users': get_users(),
        'players': get_players(),
        'owner': get_owner()
    }

def get_attend_message(user,datetime):
    return {
        'text': GameMessageCommand.ATTEND,
        'datetime': datetime.strftime("%Y-%m-%d %H:%M:%S%z"),
        'sender': {
            'uid': user.id,
            'nickname': user.last_name
        },
        'type': MessageType.GAME,
        'users': get_users(),
        'players': get_players(),
        'owner': get_owner()
    }


def get_offline_message(user, datetime):
    return {
        'text': SystemMessageText.OFFLINE,
        'datetime': datetime.strftime("%Y-%m-%d %H:%M:%S%z"),
        'sender': {
            'uid': user.id,
            'nickname': user.last_name
        },
        'type': MessageType.SYSTEM,
        'users': get_users(),
        'players': get_players(),
        'owner': get_owner()
    }


def get_user_list_message():
    return {
        'text': SystemMessageText.USER_LIST,
        'datetime': timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
        'type': MessageType.SYSTEM,
        'users': get_users(),
        'players': get_players(),
        'owner': get_owner()
    }


def get_player_list_message():
    return {
        'text': SystemMessageText.USER_LIST,
        'datetime': timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
        'type': MessageType.SYSTEM,
        'users': get_users(),
        'players': get_players(),
        'owner': get_owner()
    }


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "ouat"
        self.room_group_name = "group_ouat"
        self.user = None
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # 自动发一下userlist
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': get_user_list_message()
            }
        )
        # 自动发一下playerlist
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': get_player_list_message()
            }
        )

    def disconnect(self, closecode):
        if self.user:
            remove_user(self.user.id)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': get_offline_message(self.user, timezone.now())
                }
            )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = None
        if self.user and self.user.is_authenticated:
            sender = self.user
        sender_id = text_data_json['sender']if 'sender' in text_data_json else None
        sender = get_user_by_id(
            sender_id) if sender_id and not sender else sender
        message_text = text_data_json['text'] if 'text' in text_data_json else None
        message_color = text_data_json['color'] if 'color' in text_data_json else None
        message_type = text_data_json['type'] if 'type' in text_data_json else None
        if sender:
            if message_type == 'system':
                if message_text == SystemMessageText.ONLINE:
                    add_user(sender.id)
                    self.user = sender
                    message = Message(
                        text=message_text,
                        datetime=timezone.now(),
                        sender=sender,
                        message_type=Message.MessageTypes.SYSTEM
                    )
                    message.save()
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': get_online_message(sender, message.datetime)
                        }
                    )
                if message_text == SystemMessageText.OFFLINE:
                    remove_user(sender.id)
                    self.user = None
                    message = Message(
                        text=message_text,
                        datetime=timezone.now(),
                        sender=sender,
                        message_type=Message.MessageTypes.SYSTEM
                    )
                    message.save()
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': get_offline_message(sender, message.datetime)
                        }
                    )
            elif message_type == 'game':
                if message_text == GameMessageCommand.ATTEND:
                    add_player(sender.id)
                    message = Message(
                        text=message_text,
                        datetime=timezone.now(),
                        sender=sender,
                        message_type=Message.MessageTypes.GAME
                    )
                    message.save()
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': get_attend_message(sender, message.datetime)
                        }
                    )
            else:
                message = Message(
                    text=message_text,
                    datetime=timezone.now(),
                    sender=sender,
                    color=message_color
                )
                message.save()
                send_message = {
                    'text': message_text,
                    'datetime': message.datetime.strftime("%Y-%m-%d %H:%M:%S%z"),
                    'sender': {
                        'uid': sender.id,
                        'nickname': sender.last_name
                    },
                    'color': message_color,
                    'type': MessageType.CHAT
                }
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': send_message
                    }
                )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
