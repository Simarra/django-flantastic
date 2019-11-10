from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.zoom_on_position, name='base'),
    path('api/v1/', views.bakeries_arround,
         name='base_api_url'),  # Abstract url
    path('api/v1/bakerie_arround/pos/<str:longlat>/',
         views.bakeries_arround, name='closest_bakeries'),
    path('api/v1/bakerie_arround_2/pos/'
          '<str:longitude>/<str:latitude>/'
          '<str:id_not_to_get>/'
          '<str:bbox_top_left>'
          '<str:bbox_top_right>'
          '<str:bbox_bottom_left>'
          '<str:bbox_bottom_right>',
         views.bakeries_arround, name='closest_bakeries'),
    path('api/v1/user_bakeries/',
         views.user_bakeries, name='closest_bakeries'),
    # formated in ajax using the previous abstract url.
    path('login/',
         auth_views.LoginView.as_view(
             template_name='flantastic/login.html'), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='flantastic/logout.html'), name='logout'),
    path('editbakerie', views.edit_bakerie, name='edit_bakerie')
]
