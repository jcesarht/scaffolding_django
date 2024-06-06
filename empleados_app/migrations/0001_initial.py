# Generated by Django 5.0.4 on 2024-06-06 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('emp_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_ingreso', models.DateTimeField()),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('salario', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'empleados',
                'managed': False,
            },
        ),
    ]
