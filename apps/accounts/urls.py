# -*- encoding: utf-8 -*-


from django.urls import path
from .views import login_view, user_add, users_list,user_edit,user_del,password_change
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('user/', users_list, name="users_list"),
    path('user/add/', user_add, name="user_add"),
    path('user/edit/<int:pk>/', user_edit, name="user_edit"),
    path('user/del/<int:pk>/', user_del, name="user_del"),
    path('user/changepasswd/<int:pk>/',password_change),
    path("logout/", LogoutView.as_view(next_page='/login/'), name="logout")
]
