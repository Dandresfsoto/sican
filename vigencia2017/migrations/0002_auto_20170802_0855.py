# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-02 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_entregable_escencial'),
        ('vigencia2017', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoContrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ValorEntregableVigencia2017',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('entregable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entregable_valor_vigencia_2017', to='productos.Entregable')),
            ],
        ),
        migrations.AddField(
            model_name='tipocontrato',
            name='entregables',
            field=models.ManyToManyField(to='vigencia2017.ValorEntregableVigencia2017'),
        ),
    ]
