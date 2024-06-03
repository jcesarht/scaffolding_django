#!/usr/bin/env python3
from rest_framework import routers
from .api import EmpleadosViewSet

router =  routers.DefaultRouter()

router.register("api/empleados", EmpleadosViewSet, "empleados" )
urlpatterns = router.urls