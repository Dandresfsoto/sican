#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from administrativos.models import Administrativo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from negociadores.models import Negociador, Soporte
from cargos.models import Cargo
from rh.models import TipoSoporte

class NegociadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NegociadorForm, self).__init__(*args, **kwargs)
        self.fields['cargo'].queryset = Cargo.objects.exclude(oculto = True)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Región',
                Div(
                    Div('region',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Datos personales',
                Div(
                    Div('nombres',css_class='col-sm-6'),
                    Div('apellidos',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('cedula',css_class='col-sm-4'),
                    Div('correo_personal',css_class='col-sm-4'),
                    Div('celular_personal',css_class='col-sm-4'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Información profesional',
                Div(
                    Div('cargo',css_class='col-sm-6'),
                    Div('profesion',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('fecha_contratacion',css_class='col-sm-6'),
                    Div('fecha_terminacion',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Seguridad social e información bancaria',
                Div(
                    Div('eps',css_class='col-sm-4'),
                    Div('pension',css_class='col-sm-4'),
                    Div('arl',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('banco',css_class='col-sm-4'),
                    Div('tipo_cuenta',css_class='col-sm-4'),
                    Div('numero_cuenta',css_class='col-sm-4'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Lider',
                Div(
                    Div('lider',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Departamentos',
                Div(
                    Div('departamentos',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Ruta',
                Div(
                    Div('codigo_ruta',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
        )

    class Meta:
        model = Negociador
        fields = '__all__'
        widgets = {
            'tipo_cuenta': forms.Select(choices=(('','---------'),
                                                 ('Ahorros','Ahorros'),
                                                 ('Corriente','Corriente'),
                                                 )
                                        ),
        }