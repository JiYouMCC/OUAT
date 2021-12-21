from django.contrib import admin
from .models import Message,Token


class Message_admin(admin.ModelAdmin):
    list_display = ('datetime', 'sender', 'receiver', 'text', 'message_type')

class Token_admin(admin.ModelAdmin):
    list_display = ('user', 'token')

admin.site.register(Message, Message_admin)
admin.site.register(Token, Token_admin)
