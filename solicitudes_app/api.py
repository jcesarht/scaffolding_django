#!/usr/bin/env python3
from rest_framework import viewsets, permissions
from .models import Solicitudes
from .serializers import SolicitudesSerializer

class SolicitudesViewSet(viewsets.ModelViewSet):
   queryset = Solicitudes.objects.all() 
   permission_classes = [permissions.AllowAny]
   serializer_class = SolicitudesSerializer
   
