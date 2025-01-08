#!/usr/bin/env python3
from django.urls import path, re_path
from django.contrib import admin
from .views import register, signin, profile
admin.autodiscover()
urlpatterns = [
    path('api/v1/USllogin/register/',register,name='login_register'),
    path('api/v1/USllogin/',signin,name='login_signin'),
    re_path(r'^api/v1/USllogin/profile/(?P<user_id_param>[\w-]+)?/?$',profile,name='login_profile'),
]