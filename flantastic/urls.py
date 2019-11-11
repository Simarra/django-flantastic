from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.zoom_on_position, name='base'),
    path('api/v1/', views.bakeries_arround,
         name='base_api_url'),  # Abstract url
    path('api/v1/bakerie_arround/pos/'
          '<str:id_not_to_get>/'
          '<str:longlat>/'
          '<str:bbox_north_east>/'
          '<str:bbox_south_west>/',
         views.bakeries_arround, name='closest_bakeries'),
    path('api/v1/user_bakeries/',
         views.user_bakeries, name='user_bakeries'),
    # formated in ajax using the previous abstract url.
    path('login/',
         auth_views.LoginView.as_view(
             template_name='flantastic/login.html'), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='flantastic/logout.html'), name='logout'),
    path('editbakerie', views.edit_bakerie, name='edit_bakerie')
]
