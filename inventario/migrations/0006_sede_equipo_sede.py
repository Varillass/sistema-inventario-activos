# Generated by Django 5.2.4 on 2025-07-25 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_remove_equipo_descripcion_equipo_observacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('direccion', models.TextField(blank=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Sede',
                'verbose_name_plural': 'Sedes',
            },
        ),
        migrations.AddField(
            model_name='equipo',
            name='sede',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipos', to='inventario.sede', verbose_name='Sede'),
        ),
    ]
