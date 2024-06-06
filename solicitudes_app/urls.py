#!/usr/bin/env python3
from rest_framework import routers
from .api import SolicitudesViewSet

router =  routers.DefaultRouter()

router.register("api/solicitudes", SolicitudesViewSet, "solicitudes" )
urlpatterns = router.urls