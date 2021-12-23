from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hall/users/', views.get_users),
    path('hall/add_user/', views.add_user)
]