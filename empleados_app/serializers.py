from rest_framework import serializers
from .models import Empleados

class EmpleadosSerializer(serializers.ModelSerializer):

   class Meta:
      model = Empleados
      field = ('emp_id', 'fecha_ingreso', 'nombre', 'salario')
      read_only_fields = ('fecha_ingreso',) 
