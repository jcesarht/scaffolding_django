#!/usr/bin/env python3
from rest_framework import viewsets, permissions
from .models import Empleados
from .serializers import EmpleadosSerializer

class EmpleadosViewSet(viewsets.ModelViewSet):
   queryset = Empleados.objects.all() 
   permission_classes = [permissions.AllowAny]
   serializer_class = EmpleadosSerializer
   
