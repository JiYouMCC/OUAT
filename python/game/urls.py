from django.urls import path

from . import views
from . import hall

urlpatterns = [
    path('', views.index, name='index')
]