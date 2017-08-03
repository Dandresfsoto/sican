#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from radicados.models import Radicado, RadicadoRetoma
from secretarias.models import Secretaria
from municipios.models import Municipio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from vigencia2017.models import DaneSEDE, Grupos, TipoContrato, ValorEntregableVigencia2017
from formadores.models import Contrato
from productos.models import Entregable


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

class ValorEntregableVigencia2017Form(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ValorEntregableVigencia2017Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout()

        entregables = Entregable.objects.filter(sesion__nivel__diplomado__id=kwargs['initial']['id_diplomado']).order_by('numero')
        tipo_contrato = TipoContrato.objects.get(id=kwargs['initial']['id_contrato'])

        nivel_count = 0
        data = {}
        field_count = 0

        for entregable in entregables:
            nombre_nivel = entregable.sesion.nivel.nombre
            nombre_sesion = entregable.sesion.nombre

            if nombre_nivel not in data.keys():
                self.helper.layout.fields.append(Fieldset(nombre_nivel))
                data[nombre_nivel] = {'position':nivel_count,'sesiones':{},'count':0}
                nivel_count += 1


            if nombre_sesion not in data[nombre_nivel]['sesiones'].keys():
                self.helper.layout.fields[ data[nombre_nivel]['position'] ].append(Fieldset("N"+str(data[nombre_nivel]['position'])+": "+nombre_sesion))
                data[nombre_nivel]['sesiones'][nombre_sesion] = {'position': data[nombre_nivel]['count']}
                data[nombre_nivel]['count'] += 1

            self.fields[str(entregable.id)] = forms.FloatField(label=str(entregable.numero)+" - "+entregable.nombre,initial=0)
            self.helper.layout.fields[data[nombre_nivel]['position']].fields[data[nombre_nivel]['sesiones'][nombre_sesion]['position']].append(Div(str(entregable.id)))


            try:
                valor = ValorEntregableVigencia2017.objects.get(entregable=entregable, tipo_contrato=tipo_contrato)
            except:
                pass
            else:
                self.fields[str(entregable.id)].initial = valor.valor