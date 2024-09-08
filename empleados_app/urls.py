#!/usr/bin/env python3
from django.urls import re_path
from .views import transaction_data

urlpatterns = [
    re_path('api/v1/empleados/',transaction_data,name = 'empleados_app_transaction'),
    re_path(r'^api/v1/empleados/(?P<user_id_param>[\w-]+)?/?$',transaction_data,name = 'empleados_app_query_or_delete'),
]