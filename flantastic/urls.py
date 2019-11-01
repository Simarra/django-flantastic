from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.zoom_on_position, name='base'),
    path('pos', views.bakeries_arround,
         name='base_closest_bakeries_url'),  # Abstract url
    path('pos/<str:longitude>/<str:latitude>/',
         views.bakeries_arround, name='closest_bakeries'),
    # formated in ajax using the previous abstract url.
    path('login/',
         auth_views.LoginView.as_view(
             template_name='flantastic/login.html'), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='flantastic/logout.html'), name='logout'),
    path('editbakerie', views.edit_bakerie, name='edit_bakerie')
]
