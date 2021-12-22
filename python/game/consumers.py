from .models import Message
from account.views import get_user_by_token, get_user_by_id
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "ouat"
        self.room_group_name = "group_ouat"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_nickname = text_data_json['sender']
        sender_token = text_data_json['token'] if 'token' in text_data_json else None
        sender_id = text_data_json['uid'] if 'uid' in text_data_json else None
        message_text = text_data_json['text']
        message_color = text_data_json['color'] if 'color' in text_data_json else None
        sender = get_user_by_token(sender_token) if sender_token else None
        sender = get_user_by_id(sender_id) if sender_id and not sender else sender
        message_type = text_data_json['type'] if 'type' in text_data_json else None
        if sender:
            if message_type == 'system':
                if message_text == 'login' or message_text == 'logout':
                    message = Message(
                        text=text_data_json['text'],
                        datetime=timezone.now(),
                        sender=sender,
                        message_type=Message.MessageTypes.SYSTEM
                    )
                    message.save()
                    send_message = {
                        'text': text_data_json['text'],
                        'datetime': message.datetime.strftime("%Y-%m-%d %H:%M%z"),
                        'sender': sender_nickname,
                        'type': 'system'
                    }
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': send_message
                        }
                    )
            else:
                message = Message(
                    text=text_data_json['text'],
                    datetime=timezone.now(),
                    sender=sender,
                    color=message_color
                )
                message.save()
                send_message = {
                    'text': text_data_json['text'],
                    'datetime': message.datetime.strftime("%Y-%m-%d %H:%M%z"),
                    'sender': sender_nickname,
                    'color': message_color,
                    'type': 'chat'
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
