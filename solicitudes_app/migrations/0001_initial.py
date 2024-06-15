# Generated by Django 5.0.4 on 2024-06-15 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitudes',
            fields=[
                ('sol_id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=50, null=True)),
                ('resumen', models.CharField(blank=True, max_length=50, null=True)),
                ('create_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'solicitudes',
                'managed': False,
            },
        ),
    ]
