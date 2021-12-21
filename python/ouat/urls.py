from django.contrib import admin
from django.urls import include, path
from . import accounts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),
    path('login/', accounts.login),
    path('register/', accounts.register),
    path('logout/', accounts.logout),
    path('change_nickname/', accounts.change_nickname),
    path('get_status/', accounts.get_status),
]