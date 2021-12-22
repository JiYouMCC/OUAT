from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('change_nickname/', views.change_nickname),
    path('get_status/', views.get_status)
]