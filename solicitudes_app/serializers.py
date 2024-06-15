from rest_framework import serializers
from .models import Solicitudes

class SolicitudesSerializer(serializers.ModelSerializer):

   class Meta:
      model = Solicitudes
      fields = ('create_at',)
      read_only_fields = ('create_at',) 
