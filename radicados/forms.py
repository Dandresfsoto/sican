#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from radicados.models import Radicado
from secretarias.models import Secretaria
from municipios.models import Municipio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML


class RadicadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RadicadoForm, self).__init__(*args, **kwargs)
        self.fields['secretaria'].queryset = Secretaria.objects.exclude(oculto = True)
        self.fields['municipio'].queryset = Municipio.objects.exclude(oculto = True)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Radicado',
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('secretaria',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('municipio',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('nombre_sede',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('dane_sede',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('tipo',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('ubicacion',css_class='col-sm-12'),
                    css_class = 'row'
                )
            )
        )

    class Meta:
        model = Radicado
        fields = '__all__'