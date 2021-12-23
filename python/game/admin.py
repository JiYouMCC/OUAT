from django.contrib import admin
from .models import Message, Cache


class Message_admin(admin.ModelAdmin):
    list_display = ('datetime', 'sender', 'receiver', 'text', 'message_type')

class Cache_admin(admin.ModelAdmin):
    list_display = ('cache_key', 'cache_value')

admin.site.register(Message, Message_admin)
admin.site.register(Cache, Cache_admin)