#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from radicados.models import Radicado, RadicadoRetoma
from secretarias.models import Secretaria
from municipios.models import Municipio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from vigencia2017.models import DaneSEDE, Grupos, TipoContrato
from formadores.models import Contrato


class DaneSEDEForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DaneSEDEForm, self).__init__(*args, **kwargs)
        self.fields['secretaria'].queryset = Secretaria.objects.exclude(oculto = True)
        self.fields['municipio'].queryset = Municipio.objects.exclude(oculto = True)
        self.fields['zona'].widget = forms.Select(choices = [('','----------'),('RURAL','RURAL'),('URBANA','URBANA')])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información Sede',
                Div(
                    Div('municipio', css_class='col-sm-6'),
                    Div('secretaria', css_class='col-sm-6'),
                    css_class='row'
                ),
                Div(
                    Div('dane_sede',css_class='col-sm-4'),
                    Div('nombre_sede',css_class='col-sm-4'),
                    Div('zona', css_class='col-sm-4'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Institución Educativa',
                Div(
                    Div('dane_ie', css_class='col-sm-6'),
                    Div('nombre_ie', css_class='col-sm-6'),
                    css_class='row'
                )
            )
        )

    class Meta:
        model = DaneSEDE
        fields = '__all__'
        labels = {
        }

class GruposForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GruposForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].initial = Contrato.objects.get(id = kwargs['initial']['id_contrato'])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información Grupo',
                Div(
                    Div('diplomado', css_class='col-sm-6'),
                    Div('numero', css_class='col-sm-6'),
                    css_class='row'
                ),
                Div(
                    Div('contrato', css_class='hidden'),
                    css_class='row'
                )
            )
        )

    class Meta:
        model = Grupos
        fields = '__all__'
        labels = {
        }

class TipoContratoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TipoContratoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información del contrato',
                Div(
                    Div('nombre', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('diplomados', css_class='col-sm-12'),
                    css_class='row'
                )
            )
        )

    class Meta:
        model = TipoContrato
        exclude = ['entregables']
        labels = {
        }