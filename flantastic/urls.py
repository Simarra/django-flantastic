from django.urls import path
from djgeojson.views import GeoJSONLayerView
from django.conf.urls import url

from . import views
from .models import Bakeries

urlpatterns = [
    path('', views.zoom_on_position, name='map'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=Bakeries), name='data')
]
