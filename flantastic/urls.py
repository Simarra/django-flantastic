from django.urls import path
from django.conf.urls import url

from . import views
from .models import Bakeries

urlpatterns = [
    path('', views.zoom_on_position, name='map'),
    path('detail', views.BoundariesGeoJSON, name='map'),
]
