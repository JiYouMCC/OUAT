from django.contrib import admin
from .models import Message


class Message_admin(admin.ModelAdmin):
    list_display = ('datetime', 'sender', 'receiver', 'text', 'message_type')

admin.site.register(Message, Message_admin)