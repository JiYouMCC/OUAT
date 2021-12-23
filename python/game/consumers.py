from .models import Message, Cache
from account.views import get_user_by_id
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
import json
from .hall import add_user, remove_user, get_users
import logging


class SystemMessageText:
    INIT = 'init'
    ONLINE = 'online'
    OFFLINE = 'offline'


class MessageType:
    SYSTEM = 'system'
    CHAT = 'chat'


def get_online_message(user, datetime):
    return {
        'text': SystemMessageText.ONLINE,
        'datetime': datetime.strftime("%Y-%m-%d %H:%M%z"),
        'sender': {
            'uid': user.id,
            'nickname': user.last_name
        },
        'type': MessageType.SYSTEM,
        'users': get_users()
    }


def get_offline_message(user, datetime):
    return {
        'text': SystemMessageText.OFFLINE,
        'datetime': datetime.strftime("%Y-%m-%d %H:%M%z"),
        'sender': {
            'uid': user.id,
            'nickname': user.last_name
        },
        'type': MessageType.SYSTEM,
        'users': get_users()
    }

def get_user_list_message():
    return {
            'text': SystemMessageText.INIT,
            'datetime': timezone.now().strftime("%Y-%m-%d %H:%M%z"),
            'type': MessageType.SYSTEM,
            'users': get_users()
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
                    'datetime': message.datetime.strftime("%Y-%m-%d %H:%M%z"),
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
