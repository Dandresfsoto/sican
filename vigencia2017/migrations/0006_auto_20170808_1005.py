# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-08 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0003_region_departamentos'),
        ('vigencia2017', '0005_auto_20170808_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeneficiarioCambio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dane_sede_text', models.CharField(blank=True, max_length=1000, null=True)),
                ('apellidos', models.CharField(max_length=100)),
                ('nombres', models.CharField(max_length=100)),
                ('cedula', models.BigIntegerField()),
                ('correo', models.EmailField(blank=True, max_length=100, null=True)),
                ('telefono_fijo', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono_celular', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.IntegerField(blank=True, null=True)),
                ('grado', models.IntegerField(blank=True, null=True)),
                ('genero', models.CharField(blank=True, max_length=100, null=True)),
                ('dane_sede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vigencia2017.DaneSEDE')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grupo_beneficiario_vigencia_2017_cambio', to='vigencia2017.Grupos')),
                ('masivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vigencia2017.CargaMatriz')),
            ],
        ),
        migrations.AlterField(
            model_name='beneficiario',
            name='dane_sede_text',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='beneficiariocambio',
            name='original',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vigencia2017.Beneficiario'),
        ),
        migrations.AddField(
            model_name='beneficiariocambio',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_beneficiario_vigencia_2017_cambio', to='region.Region'),
        ),
    ]