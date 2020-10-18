from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
        path('', home, name='home'),
        path('home', home, name='home'),
        path('api/get-seasons', getSeasons, name='getSeasons'),
        path('api/get-statistics/<int:season>', getStatistics, name='getStatistics'),
]


from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

