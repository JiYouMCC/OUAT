from django.contrib import admin
from .models import Message, Cache, ElementCard, EndingCard


class Message_admin(admin.ModelAdmin):
    list_display = ('datetime', 'sender', 'receiver', 'text', 'message_type')

class Cache_admin(admin.ModelAdmin):
    list_display = ('cache_key', 'cache_value')

class ElementCard_admin(admin.ModelAdmin):
    list_display = ('word', 'enable')

class EndingCard_admin(admin.ModelAdmin):
    list_display = ('text', 'enable')

admin.site.register(Message, Message_admin)
admin.site.register(Cache, Cache_admin)
admin.site.register(ElementCard, ElementCard_admin)
admin.site.register(EndingCard, EndingCard_admin)