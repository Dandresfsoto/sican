# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-03 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vigencia2017', '0003_tipocontrato_diplomados'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipocontrato',
            name='entregables',
        ),
        migrations.AddField(
            model_name='valorentregablevigencia2017',
            name='tipo_contrato',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vigencia2017.TipoContrato'),
            preserve_default=False,
        ),
    ]
