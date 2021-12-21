from . import models
from .token import get_user_by_token
from asgiref.sync import async_to_sync
from channels.auth import login
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
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
        sender_token = text_data_json['token']
        message_text = text_data_json['text']
        message_color = text_data_json['color']
        sender = get_user_by_token(sender_token)
        if sender:
            message = models.Message(
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
                'type': 'test'
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
