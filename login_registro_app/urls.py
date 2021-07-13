from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('login', views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('registro', views.new_user, name='registro'),
    path('admin', views.admin, name = 'admin'),
    #path('shows/<int:id_show>/view', views.view_show, name='view_show'),
    #path('shows/<int:id_show>/edit', views.edit_show, name='edit_show'),
    #path('shows/<int:id_show>/delete', views.delete_show, name='delete_show'),
]
