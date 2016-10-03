#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from requerimientos.models import Requerimiento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML


class RequerimientoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequerimientoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información del requerimiento',
                Div(
                    Div('recepcion_solicitud',css_class='col-sm-6'),
                    Div('region',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('entidad_remitente',css_class='col-sm-6'),
                    Div('funcionario_remitente',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('nombre',css_class='col-sm-4'),
                    Div(
                    HTML(
                        """
                        <file-upload-sican style="margin-left:14px;" name="archivo_solicitud" old_file="{{old_file}}"
                        link_old_file="{{link_old_file}}">Archivo</file-upload-sican>
                        """),
                        css_class = 'col-sm-8'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Delegación',
                Div(
                    Div('tiempo_respuesta',css_class='col-sm-4'),
                    Div('encargados',css_class='col-sm-8'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Requerimiento
        fields = '__all__'
        widgets = {
            'entidad_remitente': forms.Select(choices = ( ('','----------'),('Andes','Andes'),('Interventoria','Interventoria')) ),
            'funcionario_remitente': forms.Select(choices= ( ('','----------'),('Formación','Formación') ))
        }
        labels = {
            'recepcion_solicitud': 'Fecha de solicitud',
            'entidad_remitente': 'Entidad remitente',
            'funcionario_remitente': 'Funcionario y/o eje'
        }