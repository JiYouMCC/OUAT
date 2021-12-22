from django.contrib import admin
from .models import Token

class Token_admin(admin.ModelAdmin):
    list_display = ('user', 'token')

admin.site.register(Token, Token_admin)
