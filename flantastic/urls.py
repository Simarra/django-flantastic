from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .api import viewsets

urlpatterns = [
    path('', views.render_map, name='base'),
    path('api/v1/', viewsets.bakeries_arround,
         name='base_api_url'),
    path('api/v1/bakerie_arround/pos/'
          '<str:id_not_to_get>/'
          '<str:longlat>/'
          '<str:bbox_north_east>/'
          '<str:bbox_south_west>/',
         viewsets.bakeries_arround, name='closest_bakeries'),
    path('api/v1/user_bakeries/',
         viewsets.user_bakeries, name='user_bakeries'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='flantastic/login.html'), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='flantastic/logout.html'), name='logout'),
    path('editbakerie', views.edit_bakerie, name='edit_bakerie'),
    path('signup', views.signup, name='signup')
]
