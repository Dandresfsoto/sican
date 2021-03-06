# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-15 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0022_beneficiario_link'),
        ('evidencias', '0033_remove_evidencia_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='red',
            name='beneficiarios',
            field=models.ManyToManyField(blank=True, related_name='beneficiarios_red', to='matrices.Beneficiario'),
        ),
        migrations.AddField(
            model_name='red',
            name='producto_final',
            field=models.BooleanField(default=False),
        ),
    ]
