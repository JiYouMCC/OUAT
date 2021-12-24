from django.urls import path

from . import views
from . import hall

urlpatterns = [
    path('', views.index, name='index'),
    path('cards/', views.cards, name='cards'),
    path('init/', views.init, name='init')
]