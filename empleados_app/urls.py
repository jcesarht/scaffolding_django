#!/usr/bin/env python3
from django.urls import re_path
from .views import transaction_data

urlpatterns = [
    re_path(r'^api/v1/empleados/(?P<id_param>[\w-]+)?/?$',transaction_data,name = 'empleados_app_query_or_delete'),
]