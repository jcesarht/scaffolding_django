#!usr/bin/env/ python3
from django.urls import path, include
from django.contrib import admin
from .views import register
admin.autodiscover()
urlpatterns = [
    path('api/login/',register,name='api/login/register/')
]