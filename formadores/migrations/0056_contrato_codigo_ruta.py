# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-01 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formadores', '0055_contrato_meta_beneficiarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='codigo_ruta',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
