from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),
    path('account/', include('account.urls')),
]