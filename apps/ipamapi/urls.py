from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.subnet_list),
    path('subnet/', views.subnet_list),
    path('subnet/add/', views.add_subnet),
    path('subnet/edit/<int:pk>/', views.subnet_edit),
    path('subnet/del/<int:pk>/', views.subnet_del),
    path('ip/', views.ip_address_list),
    path('ip/add/', views.ip_address_add),
    path('ip/edit/<int:pk>/', views.ip_address_edit),
    path('ip/del/<int:pk>/', views.ip_address_del),
    path('show/<int:pk>/', views.ip_show),
]
