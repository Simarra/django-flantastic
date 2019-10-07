from django.urls import path
from django.conf.urls import url

from . import views
from .models import Bakeries

urlpatterns = [
    path('', views.zoom_on_position, name='base'),
    path('map', views.bakeries_arround, name='map'),
    path('<int:longitude><int:latitude>/',
         views.bakeries_arround, name='detail'),
]
