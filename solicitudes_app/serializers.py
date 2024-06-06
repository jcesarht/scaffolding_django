from rest_framework import serializers
from .models import Solicitudes

class SolicitudesSerializer(serializers.ModelSerializer):

   class Meta:
      model = Solicitudes
      fields = ('sol_id', 'codigo', 'descripcion', 'resumen', 'id_empleado', 'create_at')
      
