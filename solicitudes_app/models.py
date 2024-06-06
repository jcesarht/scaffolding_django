# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from empleados_app.models import Empleados

class Solicitudes(models.Model):
    sol_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    resumen = models.CharField(max_length=50, blank=True, null=True)
    id_empleado = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_empleado')
    create_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        app_label = 'solicitudes_app'
        managed = False
        db_table = 'solicitudes'
