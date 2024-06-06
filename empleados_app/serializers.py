from rest_framework import serializers
from .models import Empleados

class EmpleadosSerializer(serializers.ModelSerializer):

   class Meta:
      model = Empleados
      fields = ('emp_id', 'fecha_ingreso', 'nombre', 'salario')
      
