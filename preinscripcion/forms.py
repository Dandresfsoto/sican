#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from preinscripcion.models import DocentesPreinscritos
from municipios.models import Municipio
from radicados.models import Radicado
from docentes.models import DocentesMinEducacion

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
                <button type="submit" class="btn btn-cpe">Consultar</button>
                """)
            ),
        )

    cedula = forms.IntegerField(label='Cedula')

class Registro(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Registro, self).__init__(*args, **kwargs)
        docente = DocentesMinEducacion.objects.get(cedula=kwargs['initial']['cedula'])

        self.fields['primer_apellido'].initial = docente.primer_apellido
        self.fields['segundo_apellido'].initial = docente.segundo_apellido
        self.fields['primer_nombre'].initial = docente.primer_nombre
        self.fields['segundo_nombre'].initial = docente.segundo_nombre
        self.fields['cedula'].initial = docente.cedula
        self.fields['cargo'].initial = docente.cargo
        self.fields['verificado'].initial = True

        if 'data' not in kwargs:
            self.fields['municipio'].widget.choices = (('','---------'),)
            self.fields['radicado'].widget.choices = (('','---------'),)


        else:
            id_departamento = kwargs['data']['departamento']
            if id_departamento == '':
                id_departamento = 0
            self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

            id_municipio = kwargs['data']['municipio']
            if id_municipio == '':
                id_municipio = 0
            self.fields['radicado'].widget.choices = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',

                HTML("""
                <p style="color:white;">Porfavor actualiza tus datos personales en el siguiente formulario:</p>
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

                Div(
                    Div('verificado',css_class='col-sm-3 col-sm-offset-2'),
                    css_class = 'hidden'
                ),


                HTML("""
                <div class="row"><button type="submit" class="btn btn-cpe">Preinscribirme</button></div>
                """)
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('Docente','Docente'),('Directivo Docente','Directivo Docente')))
        }

class PregistroForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PregistroForm, self).__init__(*args, **kwargs)

        self.fields['cedula'].initial = kwargs['initial']['cedula']
        self.fields['verificado'].initial = False

        if 'data' not in kwargs:
            self.fields['municipio'].widget.choices = (('','---------'),)
            self.fields['radicado'].widget.choices = (('','---------'),)

        else:
            id_departamento = kwargs['data']['departamento']
            if id_departamento == '':
                id_departamento = 0
            self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

            id_municipio = kwargs['data']['municipio']
            if id_municipio == '':
                id_municipio = 0
            self.fields['radicado'].widget.choices = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',

                HTML("""
                <h3>No se ha encontrado tu numero de cedula en la base de datos de docentes.</h3>
                <p style="color:white;">Por favor completa el siguiente formulario para comprobar con la secretaria de educación
                tu vinculación.</p>
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

                Div(
                    Div('verificado',css_class='col-sm-3 col-sm-offset-2'),
                    css_class = 'hidden'
                ),


                HTML("""
                <div class="row"><button type="submit" class="btn btn-cpe">Preinscribirme</button></div>
                """)
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('Docente','Docente'),('Directivo Docente','Directivo Docente')))
        }

class UpdateRegistroForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateRegistroForm, self).__init__(*args, **kwargs)
        id_departamento = self.initial['departamento']
        if id_departamento == '':
            id_departamento = 0
        self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

        id_municipio = self.initial['municipio']
        if id_municipio == '':
            id_municipio = 0
        self.fields['radicado'].widget.choices = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',

                HTML("""
                <p style="color:white;">Si lo requieres actualiza tus datos personales en el siguiente formulario:</p>
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
                <button type="submit" class="btn btn-cpe">Actualizar</button>
                """)
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('Docente','Docente'),('Directivo docente','Directivo docente')))
        }