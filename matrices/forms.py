#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from matrices.models import Beneficiario
from region.models import Region
from productos.models import Diplomado
from radicados.models import Radicado
from formadores.models import Grupos, Formador
from matrices.models import CargaMasiva
from usuarios.models import User

class BeneficiarioForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(BeneficiarioForm, self).clean()
        radicado_text = cleaned_data.get('radicado_text')
        diplomado = cleaned_data.get('diplomado')
        area = cleaned_data.get('area')
        grado = cleaned_data.get('grado')

        if diplomado.nombre != 'ESCUELA TIC FAMILIA':
            if radicado_text == '':
                self.add_error('radicado_text','Este campo es requerido.')

            try:
                radicado = Radicado.objects.get(numero = radicado_text)
            except:
                radicado = ''

            if radicado == '':
                self.add_error('radicado_text','No existe este numero de radicado')

        else:
            pass


    def __init__(self, *args, **kwargs):
        super(BeneficiarioForm, self).__init__(*args, **kwargs)
        diplomado_nombre = kwargs['initial']['diplomado_nombre']

        if diplomado_nombre == 'INNOVATIC':
            numero = 1
        elif diplomado_nombre == 'TECNOTIC':
            numero = 2
        elif diplomado_nombre == 'DIRECTIC':
            numero = 3
        elif diplomado_nombre == 'ESCUELA TIC FAMILIA':
            numero = 4
        elif diplomado_nombre == 'ESCUELATIC':
            numero = 4
        else:
            numero = 0

        if numero == 4:
            self.fields['radicado_text'].widget = forms.HiddenInput()
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['grado'].widget = forms.HiddenInput()

        self.fields['grupo'].widget.choices = (('','----------'),)
        self.fields['diplomado'].initial = Diplomado.objects.get(numero=numero)

        if 'data' in kwargs.keys():
            if kwargs['data']['formador'] != '':
                formador = Formador.objects.get(id=kwargs['data']['formador'])
                choices = []
                for choice in Grupos.objects.filter(formador=formador):
                    choices.append((choice.id,choice.formador.codigo_ruta + '-' + choice.nombre))
                self.fields['grupo'].choices = choices


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos Generales',
                Div(
                    Div('diplomado',css_class='col-sm-4'),
                    css_class = 'hidden'
                ),
                Div(
                    Div('region',css_class='col-sm-4'),
                    Div('formador',css_class='col-sm-4'),
                    Div('grupo',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('radicado_text',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Datos personales',
                Div(
                    Div('apellidos',css_class='col-sm-4'),
                    Div('nombres',css_class='col-sm-4'),
                    Div('cedula',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('correo',css_class='col-sm-4'),
                    Div('telefono_fijo',css_class='col-sm-4'),
                    Div('telefono_celular',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('area',css_class='col-sm-6'),
                    Div('grado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('genero',css_class='col-sm-6'),
                    Div('estado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Beneficiario
        fields = '__all__'
        widgets = {
            'estado': forms.Select(choices=(('','----------'),('Activo','Activo'),('Conformación de grupo','Conformación de grupo'),('Retirado','Retirado'))),
            'genero': forms.Select(choices=(('','----------'),('Femenino','Femenino'),('Masculino','Masculino')))
        }
        labels = {
            'radicado_text': 'Radicado*',
            'area':'Area',
            'grado':'Grado'
        }

class BeneficiarioUpdateForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(BeneficiarioUpdateForm, self).clean()
        radicado_text = cleaned_data.get('radicado_text')
        diplomado = cleaned_data.get('diplomado')
        area = cleaned_data.get('area')
        grado = cleaned_data.get('grado')

        if diplomado.nombre != 'ESCUELA TIC FAMILIA' or diplomado.nombre != 'ESCUELATIC':
            if radicado_text == '':
                self.add_error('radicado_text','Este campo es requerido.')

            try:
                radicado = Radicado.objects.get(numero = radicado_text)
            except:
                radicado = ''

            if radicado == '':
                self.add_error('radicado_text','No existe este numero de radicado')

        else:
            pass

    def __init__(self, *args, **kwargs):
        super(BeneficiarioUpdateForm, self).__init__(*args, **kwargs)
        diplomado_nombre = kwargs['initial']['diplomado_nombre']

        if diplomado_nombre == 'INNOVATIC':
            numero = 1
        elif diplomado_nombre == 'TECNOTIC':
            numero = 2
        elif diplomado_nombre == 'DIRECTIC':
            numero = 3
        elif diplomado_nombre == 'ESCUELA TIC FAMILIA':
            numero = 4
        elif diplomado_nombre == 'ESCUELATIC':
            numero = 4
        else:
            numero = 0

        if numero == 4:
            self.fields['radicado_text'].widget = forms.HiddenInput()
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['grado'].widget = forms.HiddenInput()

        self.fields['grupo'].widget.choices = (('','----------'),)
        self.fields['diplomado'].initial = Diplomado.objects.get(numero=numero)

        formador = Formador.objects.get(id=kwargs['initial']['formador_id'])
        choices = []
        for choice in Grupos.objects.filter(formador=formador):
            choices.append((choice.id,choice.formador.codigo_ruta + '-' + choice.nombre))
        self.fields['grupo'].choices = choices


        if 'data' in kwargs.keys():
            if kwargs['data']['formador'] != '':
                formador = Formador.objects.get(id=kwargs['data']['formador'])
                choices = []
                for choice in Grupos.objects.filter(formador=formador):
                    choices.append((choice.id,choice.formador.codigo_ruta + '-' + choice.nombre))
                self.fields['grupo'].choices = choices


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos Generales',
                Div(
                    Div('diplomado',css_class='col-sm-4'),
                    css_class = 'hidden'
                ),
                Div(
                    Div('region',css_class='col-sm-4'),
                    Div('formador',css_class='col-sm-4'),
                    Div('grupo',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('radicado_text',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Datos personales',
                Div(
                    Div('apellidos',css_class='col-sm-4'),
                    Div('nombres',css_class='col-sm-4'),
                    Div('cedula',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('correo',css_class='col-sm-4'),
                    Div('telefono_fijo',css_class='col-sm-4'),
                    Div('telefono_celular',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('area',css_class='col-sm-6'),
                    Div('grado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('genero',css_class='col-sm-6'),
                    Div('estado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Beneficiario
        fields = '__all__'
        widgets = {
            'estado': forms.Select(choices=(('','----------'),('Activo','Activo'),('Conformación de grupo','Conformación de grupo'),('Retirado','Retirado'))),
            'genero': forms.Select(choices=(('','----------'),('Femenino','Femenino'),('Masculino','Masculino')))
        }
        labels = {
            'radicado_text': 'Radicado*',
            'area':'Area',
            'grado':'Grado'
        }

class CargaMasivaForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(CargaMasivaForm, self).clean()
        archivo = cleaned_data.get('archivo')
        if archivo.content_type != u'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            self.add_error('archivo','Se debe seleccionar un archivo excel.')


    def __init__(self, *args, **kwargs):
        super(CargaMasivaForm, self).__init__(*args, **kwargs)

        self.fields['usuario'].initial = User.objects.get(id = kwargs['initial']['id_usuario'])
        self.fields['usuario'].widget = forms.HiddenInput()

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Carga masiva de matrices',
                Div(
                    HTML("""
                            <file-upload-sican style="margin-left:14px;" name="archivo">Archivo</file-upload-sican>
                        """),
                    css_class = 'row'
                ),
                Div(
                    'archivo',
                    css_class = 'hidden'
                )
            ),
        )

    class Meta:
        model = CargaMasiva
        fields = ['usuario','archivo']