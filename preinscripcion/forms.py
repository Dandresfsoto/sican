#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from preinscripcion.models import DocentesPreinscritos

class Consulta(forms.Form):

    def __init__(self, *args, **kwargs):
        super(Consulta, self).__init__(*args, **kwargs)
        self.fields['cedula'].label = "Digita tu numero de cédula (sin puntos o comas)"
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div('cedula',css_class='col-sm-4 col-sm-offset-4'),
                    css_class = 'row'
                ),
                HTML("""
                <button type="submit" class="btn btn-primary">Consultar</button>
                """)
            ),
        )

    cedula = forms.IntegerField(label='Cedula')

class Registro(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Registro, self).__init__(*args, **kwargs)
        self.fields['municipio'].widget.choices = (('','---------'),)
        self.fields['radicado'].widget.choices = (('','---------'),)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',

                HTML("""
                <p style="color:white;">Porfavor actualice sus datos personales en el siguiente formulario:</p>
                <br>
                """),

                Div(
                    Div('primer_apellido',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_apellido',css_class='col-sm-4'),
                    css_class = 'row'
                ),


                Div(
                    Div('primer_nombre',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_nombre',css_class='col-sm-4'),
                    css_class = 'row'
                ),



                Div(
                    Div('cedula',css_class='col-sm-4 col-sm-offset-2'),
                    Div('cargo',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('correo',css_class='col-sm-3 col-sm-offset-2'),
                    Div('telefono_fijo',css_class='col-sm-3'),
                    Div('telefono_celular',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('departamento',css_class='col-sm-3 col-sm-offset-2'),
                    Div('municipio',css_class='col-sm-3'),
                    Div('radicado',css_class='col-sm-2'),
                    css_class = 'row'
                ),


                HTML("""
                <button type="submit" class="btn btn-primary">Preinscribirme</button>
                """)
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'