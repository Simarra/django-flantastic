from django.urls import path
from . import views

urlpatterns = [
    path('', views.zoom_on_position, name='base'),
    path('pos', views.bakeries_arround,
         name='base_closest_bakeries_url'),  # Abstract url
    path('pos/<str:longitude>/<str:latitude>/',
         views.bakeries_arround, name='closest_bakeries'),
         # formated in ajax using the previous abstract url.
]
