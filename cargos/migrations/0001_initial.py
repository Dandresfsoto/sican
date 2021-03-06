# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 15:50
from __future__ import unicode_literals

from django.db import migrations, models

def create_initial(apps, schema_editor):
    Cargo = apps.get_model("cargos","Cargo")
    new = Cargo(nombre="Sin cargo", oculto = True)
    new.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.TextField(blank=True, max_length=1000)),
                ('manual', models.FileField(blank=True, upload_to='Manual Funciones')),
                ('oculto', models.BooleanField(default=False)),
            ],
        ),

        migrations.RunPython(create_initial),
    ]
