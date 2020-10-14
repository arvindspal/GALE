from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
        path('', home, name='home'),
        path('home', home, name='home'),
        path('season/<int:season>', get_season_data, name='get_season_data'),

]


from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

