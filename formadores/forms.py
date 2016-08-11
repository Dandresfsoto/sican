#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from administrativos.models import Administrativo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from formadores.models import Formador
from cargos.models import Cargo
from rh.models import TipoSoporte
from formadores.models import Soporte
from django.forms.models import modelformset_factory
from formadores.models import Soporte
from departamentos.models import Departamento
from municipios.models import Municipio
from formadores.models import SolicitudTransporte
import locale

class FormadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormadorForm, self).__init__(*args, **kwargs)
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
        )

    class Meta:
        model = Formador
        fields = '__all__'
        widgets = {
            'tipo_cuenta': forms.Select(choices=(('','---------'),
                                                 ('Ahorros','Ahorros'),
                                                 ('Corriente','Corriente'),
                                                 )
                                        ),
        }

class NuevoSoporteFormadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NuevoSoporteFormadorForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].queryset = TipoSoporte.objects.exclude(oculto = True)
        if 'data' in kwargs:
            kwargs['data']['formador'] = kwargs['initial']['formador']
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Soporte:',
                Div(
                    Div('fecha',css_class='col-sm-6'),
                    Div('tipo',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    HTML("""
                            <file-upload-sican style="margin-left:14px;" name="archivo" old_file="{{old_file}}"
                            link_old_file="{{link_old_file}}">Archivo</file-upload-sican>
                        """),
                    css_class = 'row'
                ),
                Div(
                    Div('administrativo',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
            ),
        )

    class Meta:
        model = Soporte
        fields = '__all__'
        widgets = {
            'tipo': forms.Select()
        }

class ConsultaFormador(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConsultaFormador, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div(
                    Div('cedula',css_class='col-xs-12'),
                    css_class = 'row'
                ),

                HTML("""
                    <div class="row"><button type="submit" class="btn btn-cpe">Consultar</button></div>
                    """),
                css_class='text-center'
            )
        )

    def clean(self):
        cleaned_data = super(ConsultaFormador, self).clean()
        cedula = cleaned_data.get('cedula')
        try:
            formador = Formador.objects.get(cedula=cedula)
        except:
            self.add_error('cedula','No hay ningun formador registrado con este numero de cedula.')


    cedula = forms.IntegerField(label="Digita tu número de cedula (sin puntos o comas)")

class LegalizacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LegalizacionForm, self).__init__(*args, **kwargs)
        dic = {
            'rut':6,
            'cedula':2,
            'policia':4,
            'procuraduria':5,
            'contraloria':11,
            'certificacion':9,
            'seguridad_social':8
        }


        soportes = Soporte.objects.filter(formador__cedula=kwargs['initial']['cedula'])

        rut = soportes.get(tipo__id=dic['rut'])
        fotocopia_cedula = soportes.get(tipo__id=dic['cedula'])
        antecedentes_judiciales = soportes.get(tipo__id=dic['policia'])
        antecedentes_procuraduria = soportes.get(tipo__id=dic['procuraduria'])
        antecedentes_contraloria = soportes.get(tipo__id=dic['contraloria'])
        certificacion = soportes.get(tipo__id=dic['certificacion'])
        seguridad_social = soportes.get(tipo__id=dic['seguridad_social'])

        self.helper = FormHelper(self)

        self.fields['rut'].initial = rut.archivo
        self.fields['fotocopia_cedula'].initial = fotocopia_cedula.archivo
        self.fields['antecedentes_judiciales'].initial = antecedentes_judiciales.archivo
        self.fields['antecedentes_procuraduria'].initial = antecedentes_procuraduria.archivo
        self.fields['antecedentes_contraloria'].initial = antecedentes_contraloria.archivo
        self.fields['certificacion'].initial = certificacion.archivo
        self.fields['seguridad_social'].initial = seguridad_social.archivo



        self.helper.layout = Layout(
            Div(
                Div(
                    Div('correo_personal',css_class='col-sm-4'),
                    Div('celular_personal',css_class='col-sm-4'),
                    Div('profesion',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('banco',css_class='col-sm-4'),
                    Div('tipo_cuenta',css_class='col-sm-4'),
                    Div('numero_cuenta',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('rut',css_class='col-sm-12 text-left'),

                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('fotocopia_cedula',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('antecedentes_judiciales',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('antecedentes_procuraduria',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('antecedentes_contraloria',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('certificacion',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('seguridad_social',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                HTML("""
                    <div class="row"><button type="submit" class="btn btn-cpe">Enviar</button></div>
                    """),
                css_class='text-center'
            )
        )

    rut = forms.FileField(label="RUT")
    fotocopia_cedula = forms.FileField(label="Fotocopia de la cedula")
    antecedentes_judiciales = forms.FileField(label="Antecedentes judiciales (Policía)")
    antecedentes_procuraduria = forms.FileField(label="Antecedentes procuraduria")
    antecedentes_contraloria = forms.FileField(label="Antecedentes contraloría")
    certificacion = forms.FileField(label="Certificación bancaria")
    seguridad_social = forms.FileField(label="Seguridad social, ARL y Pensión de Agosto (opcional)",required=False)

    class Meta:
        model = Formador
        fields = ['correo_personal','celular_personal','profesion','banco','tipo_cuenta','numero_cuenta']
        widgets = {
            'tipo_cuenta': forms.Select(choices=(('','---------'),
                                                 ('Ahorros','Ahorros'),
                                                 ('Corriente','Corriente'),
                                                 )
                                        ,attrs={'required':'required'}),

            'correo_personal': forms.EmailInput(attrs={'required':'required'}),
            'celular_personal': forms.TextInput(attrs={'required':'required'}),
            'profesion': forms.TextInput(attrs={'required':'required'}),
            'banco': forms.Select(attrs={'required':'required'}),
            'numero_cuenta': forms.TextInput(attrs={'required':'required'}),
        }

        labels = {
            'correo_personal':'Email personal*',
            'celular_personal':'Numero de celular*',
            'profesion':'Profesión*',
            'banco':'Banco*',
            'tipo_cuenta':'Tipo cuenta*',
            'numero_cuenta':'Numero de cuenta*'
        }

class NuevaSolicitudTransportes(forms.Form):
    nombre = forms.CharField(label="Nombre de la solicitud",max_length=20)

    fecha_1 = forms.DateField(label="Fecha")
    departamento_origen_1 = forms.CharField(label="Departamento (origen)",widget=forms.Select())
    municipio_origen_1 = forms.CharField(label="Municipio (origen)",widget=forms.Select())
    departamento_destino_1 = forms.CharField(label="Departamento (destino)",widget=forms.Select())
    municipio_destino_1 = forms.CharField(label="Municipio (destino)",widget=forms.Select())
    valor_1 = forms.CharField(label="Valor ($)")

    fecha_2 = forms.DateField(label="",required=False)
    departamento_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_2 = forms.CharField(label="",required=False)

    fecha_3 = forms.DateField(label="",required=False)
    departamento_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_3 = forms.CharField(label="",required=False)

    fecha_4 = forms.DateField(label="",required=False)
    departamento_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_4 = forms.CharField(label="",required=False)

    fecha_5 = forms.DateField(label="",required=False)
    departamento_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_5 = forms.CharField(label="",required=False)

    fecha_6 = forms.DateField(label="",required=False)
    departamento_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_6 = forms.CharField(label="",required=False)

    fecha_7 = forms.DateField(label="",required=False)
    departamento_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_7 = forms.CharField(label="",required=False)

    fecha_8 = forms.DateField(label="",required=False)
    departamento_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_8 = forms.CharField(label="",required=False)

    fecha_9 = forms.DateField(label="",required=False)
    departamento_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_9 = forms.CharField(label="",required=False)

    fecha_10 = forms.DateField(label="",required=False)
    departamento_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_10 = forms.CharField(label="",required=False)


    def __init__(self, *args, **kwargs):
        super(NuevaSolicitudTransportes, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if 'data' in kwargs.keys():
            if kwargs['data']['departamento_origen_1'] != '':
                departamento_id = kwargs['data']['departamento_origen_1']
                self.fields['municipio_origen_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_2'] != '':
                departamento_id = kwargs['data']['departamento_origen_2']
                self.fields['municipio_origen_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_3'] != '':
                departamento_id = kwargs['data']['departamento_origen_3']
                self.fields['municipio_origen_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_4'] != '':
                departamento_id = kwargs['data']['departamento_origen_4']
                self.fields['municipio_origen_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_5'] != '':
                departamento_id = kwargs['data']['departamento_origen_5']
                self.fields['municipio_origen_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_6'] != '':
                departamento_id = kwargs['data']['departamento_origen_6']
                self.fields['municipio_origen_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_7'] != '':
                departamento_id = kwargs['data']['departamento_origen_7']
                self.fields['municipio_origen_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_8'] != '':
                departamento_id = kwargs['data']['departamento_origen_8']
                self.fields['municipio_origen_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_9'] != '':
                departamento_id = kwargs['data']['departamento_origen_9']
                self.fields['municipio_origen_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_10'] != '':
                departamento_id = kwargs['data']['departamento_origen_10']
                self.fields['municipio_origen_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')







            if kwargs['data']['departamento_destino_1'] != '':
                departamento_id = kwargs['data']['departamento_destino_1']
                self.fields['municipio_destino_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_2'] != '':
                departamento_id = kwargs['data']['departamento_destino_2']
                self.fields['municipio_destino_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_3'] != '':
                departamento_id = kwargs['data']['departamento_destino_3']
                self.fields['municipio_destino_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_4'] != '':
                departamento_id = kwargs['data']['departamento_destino_4']
                self.fields['municipio_destino_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_5'] != '':
                departamento_id = kwargs['data']['departamento_destino_5']
                self.fields['municipio_destino_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_6'] != '':
                departamento_id = kwargs['data']['departamento_destino_6']
                self.fields['municipio_destino_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_7'] != '':
                departamento_id = kwargs['data']['departamento_destino_7']
                self.fields['municipio_destino_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_8'] != '':
                departamento_id = kwargs['data']['departamento_destino_8']
                self.fields['municipio_destino_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_9'] != '':
                departamento_id = kwargs['data']['departamento_destino_9']
                self.fields['municipio_destino_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_10'] != '':
                departamento_id = kwargs['data']['departamento_destino_10']
                self.fields['municipio_destino_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

        departamentos_queryset = Departamento.objects.values_list('id','nombre')
        departamentos = [('','---------')]

        for y in departamentos_queryset:
            departamentos.append((str(y[0]),y[1]))


        self.fields['departamento_origen_1'].widget.choices = departamentos
        self.fields['departamento_origen_2'].widget.choices = departamentos
        self.fields['departamento_origen_3'].widget.choices = departamentos
        self.fields['departamento_origen_4'].widget.choices = departamentos
        self.fields['departamento_origen_5'].widget.choices = departamentos
        self.fields['departamento_origen_6'].widget.choices = departamentos
        self.fields['departamento_origen_7'].widget.choices = departamentos
        self.fields['departamento_origen_8'].widget.choices = departamentos
        self.fields['departamento_origen_9'].widget.choices = departamentos
        self.fields['departamento_origen_10'].widget.choices = departamentos


        self.fields['departamento_destino_1'].widget.choices = departamentos
        self.fields['departamento_destino_2'].widget.choices = departamentos
        self.fields['departamento_destino_3'].widget.choices = departamentos
        self.fields['departamento_destino_4'].widget.choices = departamentos
        self.fields['departamento_destino_5'].widget.choices = departamentos
        self.fields['departamento_destino_6'].widget.choices = departamentos
        self.fields['departamento_destino_7'].widget.choices = departamentos
        self.fields['departamento_destino_8'].widget.choices = departamentos
        self.fields['departamento_destino_9'].widget.choices = departamentos
        self.fields['departamento_destino_10'].widget.choices = departamentos


        self.helper.layout = Layout(
            Div(
                Div(
                    Div('nombre',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_1',css_class='col-sm-2'),
                    Div('departamento_origen_1',css_class='col-sm-2'),
                    Div('municipio_origen_1',css_class='col-sm-2'),
                    Div('departamento_destino_1',css_class='col-sm-2'),
                    Div('municipio_destino_1',css_class='col-sm-2'),
                    Div('valor_1',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_2',css_class='col-sm-2'),
                    Div('departamento_origen_2',css_class='col-sm-2'),
                    Div('municipio_origen_2',css_class='col-sm-2'),
                    Div('departamento_destino_2',css_class='col-sm-2'),
                    Div('municipio_destino_2',css_class='col-sm-2'),
                    Div('valor_2',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_3',css_class='col-sm-2'),
                    Div('departamento_origen_3',css_class='col-sm-2'),
                    Div('municipio_origen_3',css_class='col-sm-2'),
                    Div('departamento_destino_3',css_class='col-sm-2'),
                    Div('municipio_destino_3',css_class='col-sm-2'),
                    Div('valor_3',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_4',css_class='col-sm-2'),
                    Div('departamento_origen_4',css_class='col-sm-2'),
                    Div('municipio_origen_4',css_class='col-sm-2'),
                    Div('departamento_destino_4',css_class='col-sm-2'),
                    Div('municipio_destino_4',css_class='col-sm-2'),
                    Div('valor_4',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_5',css_class='col-sm-2'),
                    Div('departamento_origen_5',css_class='col-sm-2'),
                    Div('municipio_origen_5',css_class='col-sm-2'),
                    Div('departamento_destino_5',css_class='col-sm-2'),
                    Div('municipio_destino_5',css_class='col-sm-2'),
                    Div('valor_5',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_6',css_class='col-sm-2'),
                    Div('departamento_origen_6',css_class='col-sm-2'),
                    Div('municipio_origen_6',css_class='col-sm-2'),
                    Div('departamento_destino_6',css_class='col-sm-2'),
                    Div('municipio_destino_6',css_class='col-sm-2'),
                    Div('valor_6',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_7',css_class='col-sm-2'),
                    Div('departamento_origen_7',css_class='col-sm-2'),
                    Div('municipio_origen_7',css_class='col-sm-2'),
                    Div('departamento_destino_7',css_class='col-sm-2'),
                    Div('municipio_destino_7',css_class='col-sm-2'),
                    Div('valor_7',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_8',css_class='col-sm-2'),
                    Div('departamento_origen_8',css_class='col-sm-2'),
                    Div('municipio_origen_8',css_class='col-sm-2'),
                    Div('departamento_destino_8',css_class='col-sm-2'),
                    Div('municipio_destino_8',css_class='col-sm-2'),
                    Div('valor_8',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_9',css_class='col-sm-2'),
                    Div('departamento_origen_9',css_class='col-sm-2'),
                    Div('municipio_origen_9',css_class='col-sm-2'),
                    Div('departamento_destino_9',css_class='col-sm-2'),
                    Div('municipio_destino_9',css_class='col-sm-2'),
                    Div('valor_9',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_10',css_class='col-sm-2'),
                    Div('departamento_origen_10',css_class='col-sm-2'),
                    Div('municipio_origen_10',css_class='col-sm-2'),
                    Div('departamento_destino_10',css_class='col-sm-2'),
                    Div('municipio_destino_10',css_class='col-sm-2'),
                    Div('valor_10',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                HTML("""
                    <div class="row"><button type="submit" class="btn btn-cpe">Enviar</button></div>
                    """),
                css_class='text-center'
            )
        )

class SolicitudTransporteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SolicitudTransporteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Solicitud de transporte:',
                Div(
                    HTML("""
                    <p>Formador: {{object.formador.nombres}} {{object.formador.apellidos}}</p>
                    <p>Solicitud: {{object.nombre}}</p>
                    <p>Valor solicitado: {{valor_solicitado}}</p>
                    <p>Archivo: <a href="{{archivo_url}}">{{archivo_nombre}}</a></p>
                    """)
                ),
                Div(
                    Div('estado',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('observacion',css_class='col-sm-12'),
                    css_class = 'row'
                )

            ),
        )

    class Meta:
        model = SolicitudTransporte
        fields = ['estado','observacion']
        widgets = {
            'estado' : forms.Select(choices=(('aprobado','Aprobado'),('consignado','Consignado'),('revision','En revisión'),('rechazado','Rechazado')))
        }

class SubirSoporteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubirSoporteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div('archivo',css_class='col-sm-12 text-left'),
                css_class = 'row'
            ),

            HTML("""
                <div class="row"><button type="submit" class="btn btn-cpe">Enviar</button></div>
            """),

        )

    class Meta:
        model = SolicitudTransporte
        fields = ['archivo']

class SolicitudTransporteAdminForm(forms.Form):
    formador = forms.CharField(label="Formador",max_length=100,widget=forms.Select())
    nombre = forms.CharField(label="Nombre de la solicitud",max_length=20)

    fecha_1 = forms.DateField(label="Fecha")
    departamento_origen_1 = forms.CharField(label="Depto (origen)",widget=forms.Select())
    municipio_origen_1 = forms.CharField(label="Municipio (origen)",widget=forms.Select())
    departamento_destino_1 = forms.CharField(label="Depto (destino)",widget=forms.Select())
    municipio_destino_1 = forms.CharField(label="Municipio (destino)",widget=forms.Select())
    valor_1 = forms.CharField(label="Valor ($)")

    fecha_2 = forms.DateField(label="",required=False)
    departamento_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_2 = forms.CharField(label="",required=False)

    fecha_3 = forms.DateField(label="",required=False)
    departamento_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_3 = forms.CharField(label="",required=False)

    fecha_4 = forms.DateField(label="",required=False)
    departamento_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_4 = forms.CharField(label="",required=False)

    fecha_5 = forms.DateField(label="",required=False)
    departamento_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_5 = forms.CharField(label="",required=False)

    fecha_6 = forms.DateField(label="",required=False)
    departamento_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_6 = forms.CharField(label="",required=False)

    fecha_7 = forms.DateField(label="",required=False)
    departamento_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_7 = forms.CharField(label="",required=False)

    fecha_8 = forms.DateField(label="",required=False)
    departamento_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_8 = forms.CharField(label="",required=False)

    fecha_9 = forms.DateField(label="",required=False)
    departamento_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_9 = forms.CharField(label="",required=False)

    fecha_10 = forms.DateField(label="",required=False)
    departamento_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_10 = forms.CharField(label="",required=False)


    def __init__(self, *args, **kwargs):
        super(SolicitudTransporteAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if 'data' in kwargs.keys():
            if kwargs['data']['departamento_origen_1'] != '':
                departamento_id = kwargs['data']['departamento_origen_1']
                self.fields['municipio_origen_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_2'] != '':
                departamento_id = kwargs['data']['departamento_origen_2']
                self.fields['municipio_origen_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_3'] != '':
                departamento_id = kwargs['data']['departamento_origen_3']
                self.fields['municipio_origen_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_4'] != '':
                departamento_id = kwargs['data']['departamento_origen_4']
                self.fields['municipio_origen_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_5'] != '':
                departamento_id = kwargs['data']['departamento_origen_5']
                self.fields['municipio_origen_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_6'] != '':
                departamento_id = kwargs['data']['departamento_origen_6']
                self.fields['municipio_origen_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_7'] != '':
                departamento_id = kwargs['data']['departamento_origen_7']
                self.fields['municipio_origen_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_8'] != '':
                departamento_id = kwargs['data']['departamento_origen_8']
                self.fields['municipio_origen_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_9'] != '':
                departamento_id = kwargs['data']['departamento_origen_9']
                self.fields['municipio_origen_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_10'] != '':
                departamento_id = kwargs['data']['departamento_origen_10']
                self.fields['municipio_origen_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')







            if kwargs['data']['departamento_destino_1'] != '':
                departamento_id = kwargs['data']['departamento_destino_1']
                self.fields['municipio_destino_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_2'] != '':
                departamento_id = kwargs['data']['departamento_destino_2']
                self.fields['municipio_destino_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_3'] != '':
                departamento_id = kwargs['data']['departamento_destino_3']
                self.fields['municipio_destino_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_4'] != '':
                departamento_id = kwargs['data']['departamento_destino_4']
                self.fields['municipio_destino_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_5'] != '':
                departamento_id = kwargs['data']['departamento_destino_5']
                self.fields['municipio_destino_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_6'] != '':
                departamento_id = kwargs['data']['departamento_destino_6']
                self.fields['municipio_destino_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_7'] != '':
                departamento_id = kwargs['data']['departamento_destino_7']
                self.fields['municipio_destino_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_8'] != '':
                departamento_id = kwargs['data']['departamento_destino_8']
                self.fields['municipio_destino_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_9'] != '':
                departamento_id = kwargs['data']['departamento_destino_9']
                self.fields['municipio_destino_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_10'] != '':
                departamento_id = kwargs['data']['departamento_destino_10']
                self.fields['municipio_destino_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

        departamentos_queryset = Departamento.objects.values_list('id','nombre')
        departamentos = [('','---------')]

        for y in departamentos_queryset:
            departamentos.append((str(y[0]),y[1]))

        formadores_queryset = Formador.objects.all().values_list('id','nombres','apellidos')
        formadores = [('','---------')]

        for y in formadores_queryset:
            formadores.append((str(y[0]),y[1]+" "+y[2]))

        self.fields['formador'].widget.choices = formadores

        self.fields['departamento_origen_1'].widget.choices = departamentos
        self.fields['departamento_origen_2'].widget.choices = departamentos
        self.fields['departamento_origen_3'].widget.choices = departamentos
        self.fields['departamento_origen_4'].widget.choices = departamentos
        self.fields['departamento_origen_5'].widget.choices = departamentos
        self.fields['departamento_origen_6'].widget.choices = departamentos
        self.fields['departamento_origen_7'].widget.choices = departamentos
        self.fields['departamento_origen_8'].widget.choices = departamentos
        self.fields['departamento_origen_9'].widget.choices = departamentos
        self.fields['departamento_origen_10'].widget.choices = departamentos


        self.fields['departamento_destino_1'].widget.choices = departamentos
        self.fields['departamento_destino_2'].widget.choices = departamentos
        self.fields['departamento_destino_3'].widget.choices = departamentos
        self.fields['departamento_destino_4'].widget.choices = departamentos
        self.fields['departamento_destino_5'].widget.choices = departamentos
        self.fields['departamento_destino_6'].widget.choices = departamentos
        self.fields['departamento_destino_7'].widget.choices = departamentos
        self.fields['departamento_destino_8'].widget.choices = departamentos
        self.fields['departamento_destino_9'].widget.choices = departamentos
        self.fields['departamento_destino_10'].widget.choices = departamentos


        self.helper.layout = Layout(
            Div(
                Div(
                    Div('formador',css_class='col-sm-6'),
                    Div('nombre',css_class='col-sm-6'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_1',css_class='col-sm-2'),
                    Div('departamento_origen_1',css_class='col-sm-2'),
                    Div('municipio_origen_1',css_class='col-sm-2'),
                    Div('departamento_destino_1',css_class='col-sm-2'),
                    Div('municipio_destino_1',css_class='col-sm-2'),
                    Div('valor_1',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_2',css_class='col-sm-2'),
                    Div('departamento_origen_2',css_class='col-sm-2'),
                    Div('municipio_origen_2',css_class='col-sm-2'),
                    Div('departamento_destino_2',css_class='col-sm-2'),
                    Div('municipio_destino_2',css_class='col-sm-2'),
                    Div('valor_2',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_3',css_class='col-sm-2'),
                    Div('departamento_origen_3',css_class='col-sm-2'),
                    Div('municipio_origen_3',css_class='col-sm-2'),
                    Div('departamento_destino_3',css_class='col-sm-2'),
                    Div('municipio_destino_3',css_class='col-sm-2'),
                    Div('valor_3',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_4',css_class='col-sm-2'),
                    Div('departamento_origen_4',css_class='col-sm-2'),
                    Div('municipio_origen_4',css_class='col-sm-2'),
                    Div('departamento_destino_4',css_class='col-sm-2'),
                    Div('municipio_destino_4',css_class='col-sm-2'),
                    Div('valor_4',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_5',css_class='col-sm-2'),
                    Div('departamento_origen_5',css_class='col-sm-2'),
                    Div('municipio_origen_5',css_class='col-sm-2'),
                    Div('departamento_destino_5',css_class='col-sm-2'),
                    Div('municipio_destino_5',css_class='col-sm-2'),
                    Div('valor_5',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_6',css_class='col-sm-2'),
                    Div('departamento_origen_6',css_class='col-sm-2'),
                    Div('municipio_origen_6',css_class='col-sm-2'),
                    Div('departamento_destino_6',css_class='col-sm-2'),
                    Div('municipio_destino_6',css_class='col-sm-2'),
                    Div('valor_6',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_7',css_class='col-sm-2'),
                    Div('departamento_origen_7',css_class='col-sm-2'),
                    Div('municipio_origen_7',css_class='col-sm-2'),
                    Div('departamento_destino_7',css_class='col-sm-2'),
                    Div('municipio_destino_7',css_class='col-sm-2'),
                    Div('valor_7',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_8',css_class='col-sm-2'),
                    Div('departamento_origen_8',css_class='col-sm-2'),
                    Div('municipio_origen_8',css_class='col-sm-2'),
                    Div('departamento_destino_8',css_class='col-sm-2'),
                    Div('municipio_destino_8',css_class='col-sm-2'),
                    Div('valor_8',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_9',css_class='col-sm-2'),
                    Div('departamento_origen_9',css_class='col-sm-2'),
                    Div('municipio_origen_9',css_class='col-sm-2'),
                    Div('departamento_destino_9',css_class='col-sm-2'),
                    Div('municipio_destino_9',css_class='col-sm-2'),
                    Div('valor_9',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_10',css_class='col-sm-2'),
                    Div('departamento_origen_10',css_class='col-sm-2'),
                    Div('municipio_origen_10',css_class='col-sm-2'),
                    Div('departamento_destino_10',css_class='col-sm-2'),
                    Div('municipio_destino_10',css_class='col-sm-2'),
                    Div('valor_10',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                css_class='text-center'
            )
        )

class SolicitudTransporteUpdateForm(forms.Form):
    formador = forms.CharField(label="Formador",max_length=100,widget=forms.Select())
    nombre = forms.CharField(label="Nombre de la solicitud",max_length=20)

    fecha_1 = forms.DateField(label="Fecha")
    departamento_origen_1 = forms.CharField(label="Depto (origen)",widget=forms.Select())
    municipio_origen_1 = forms.CharField(label="Municipio (origen)",widget=forms.Select())
    departamento_destino_1 = forms.CharField(label="Depto (destino)",widget=forms.Select())
    municipio_destino_1 = forms.CharField(label="Municipio (destino)",widget=forms.Select())
    valor_1 = forms.CharField(label="Valor ($)")
    id_1 = forms.CharField(max_length=100,widget=forms.HiddenInput())

    fecha_2 = forms.DateField(label="",required=False)
    departamento_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_2 = forms.CharField(label="",required=False)
    id_2 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_3 = forms.DateField(label="",required=False)
    departamento_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_3 = forms.CharField(label="",required=False)
    id_3 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_4 = forms.DateField(label="",required=False)
    departamento_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_4 = forms.CharField(label="",required=False)
    id_4 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_5 = forms.DateField(label="",required=False)
    departamento_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_5 = forms.CharField(label="",required=False)
    id_5 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_6 = forms.DateField(label="",required=False)
    departamento_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_6 = forms.CharField(label="",required=False)
    id_6 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_7 = forms.DateField(label="",required=False)
    departamento_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_7 = forms.CharField(label="",required=False)
    id_7 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_8 = forms.DateField(label="",required=False)
    departamento_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_8 = forms.CharField(label="",required=False)
    id_8 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_9 = forms.DateField(label="",required=False)
    departamento_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_9 = forms.CharField(label="",required=False)
    id_9 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_10 = forms.DateField(label="",required=False)
    departamento_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_10 = forms.CharField(label="",required=False)
    id_10 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)


    def __init__(self, *args, **kwargs):
        super(SolicitudTransporteUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if 'data' in kwargs.keys():
            if kwargs['data']['departamento_origen_1'] != '':
                departamento_id = kwargs['data']['departamento_origen_1']
                self.fields['municipio_origen_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            try:
                if kwargs['data']['departamento_origen_2'] != '':
                    departamento_id = kwargs['data']['departamento_origen_2']
                    self.fields['municipio_origen_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_3'] != '':
                    departamento_id = kwargs['data']['departamento_origen_3']
                    self.fields['municipio_origen_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_4'] != '':
                    departamento_id = kwargs['data']['departamento_origen_4']
                    self.fields['municipio_origen_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_5'] != '':
                    departamento_id = kwargs['data']['departamento_origen_5']
                    self.fields['municipio_origen_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_6'] != '':
                    departamento_id = kwargs['data']['departamento_origen_6']
                    self.fields['municipio_origen_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_7'] != '':
                    departamento_id = kwargs['data']['departamento_origen_7']
                    self.fields['municipio_origen_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_8'] != '':
                    departamento_id = kwargs['data']['departamento_origen_8']
                    self.fields['municipio_origen_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_9'] != '':
                    departamento_id = kwargs['data']['departamento_origen_9']
                    self.fields['municipio_origen_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_10'] != '':
                    departamento_id = kwargs['data']['departamento_origen_10']
                    self.fields['municipio_origen_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass





            try:
                if kwargs['data']['departamento_destino_1'] != '':
                    departamento_id = kwargs['data']['departamento_destino_1']
                    self.fields['municipio_destino_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_2'] != '':
                    departamento_id = kwargs['data']['departamento_destino_2']
                    self.fields['municipio_destino_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_3'] != '':
                    departamento_id = kwargs['data']['departamento_destino_3']
                    self.fields['municipio_destino_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_4'] != '':
                    departamento_id = kwargs['data']['departamento_destino_4']
                    self.fields['municipio_destino_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_5'] != '':
                    departamento_id = kwargs['data']['departamento_destino_5']
                    self.fields['municipio_destino_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_6'] != '':
                    departamento_id = kwargs['data']['departamento_destino_6']
                    self.fields['municipio_destino_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_7'] != '':
                    departamento_id = kwargs['data']['departamento_destino_7']
                    self.fields['municipio_destino_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_8'] != '':
                    departamento_id = kwargs['data']['departamento_destino_8']
                    self.fields['municipio_destino_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_9'] != '':
                    departamento_id = kwargs['data']['departamento_destino_9']
                    self.fields['municipio_destino_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_10'] != '':
                    departamento_id = kwargs['data']['departamento_destino_10']
                    self.fields['municipio_destino_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
        departamentos_queryset = Departamento.objects.values_list('id','nombre')
        departamentos = [('','---------')]

        for y in departamentos_queryset:
            departamentos.append((str(y[0]),y[1]))

        formadores_queryset = Formador.objects.all().values_list('id','nombres','apellidos')
        formadores = [('','---------')]

        for y in formadores_queryset:
            formadores.append((str(y[0]),y[1]+" "+y[2]))

        self.fields['formador'].widget.choices = formadores

        self.fields['departamento_origen_1'].widget.choices = departamentos
        self.fields['departamento_origen_2'].widget.choices = departamentos
        self.fields['departamento_origen_3'].widget.choices = departamentos
        self.fields['departamento_origen_4'].widget.choices = departamentos
        self.fields['departamento_origen_5'].widget.choices = departamentos
        self.fields['departamento_origen_6'].widget.choices = departamentos
        self.fields['departamento_origen_7'].widget.choices = departamentos
        self.fields['departamento_origen_8'].widget.choices = departamentos
        self.fields['departamento_origen_9'].widget.choices = departamentos
        self.fields['departamento_origen_10'].widget.choices = departamentos


        self.fields['departamento_destino_1'].widget.choices = departamentos
        self.fields['departamento_destino_2'].widget.choices = departamentos
        self.fields['departamento_destino_3'].widget.choices = departamentos
        self.fields['departamento_destino_4'].widget.choices = departamentos
        self.fields['departamento_destino_5'].widget.choices = departamentos
        self.fields['departamento_destino_6'].widget.choices = departamentos
        self.fields['departamento_destino_7'].widget.choices = departamentos
        self.fields['departamento_destino_8'].widget.choices = departamentos
        self.fields['departamento_destino_9'].widget.choices = departamentos
        self.fields['departamento_destino_10'].widget.choices = departamentos

        solicitud = SolicitudTransporte.objects.get(id=kwargs['initial']['pk'])
        desplazamientos = solicitud.desplazamientos.all()

        i = 0

        self.fields['formador'].initial = solicitud.formador.id
        self.fields['nombre'].initial = solicitud.nombre

        for desplazamiento in desplazamientos:
            i += 1
            self.fields['id_'+str(i)].initial = desplazamiento.id
            self.fields['fecha_'+str(i)].initial = desplazamiento.fecha
            self.fields['departamento_origen_'+str(i)].initial = desplazamiento.departamento_origen.id
            self.fields['municipio_origen_'+str(i)].widget.choices = Municipio.objects.filter(departamento__id=desplazamiento.departamento_origen.id).values_list('id','nombre')
            self.fields['municipio_origen_'+str(i)].initial = desplazamiento.municipio_origen.id
            self.fields['departamento_destino_'+str(i)].initial = desplazamiento.departamento_destino.id
            self.fields['municipio_destino_'+str(i)].widget.choices = Municipio.objects.filter(departamento__id=desplazamiento.departamento_destino.id).values_list('id','nombre')
            self.fields['municipio_destino_'+str(i)].initial = desplazamiento.municipio_destino.id
            self.fields['valor_'+str(i)].initial = "{:,}".format(float(str(round(desplazamiento.valor)))) + '0'

        for y in range(i,10):
            i += 1
            self.fields['id_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['fecha_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['departamento_origen_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio_origen_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio_origen_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['departamento_destino_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio_destino_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio_destino_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['valor_'+str(i)].widget.attrs['disabled'] = 'disabled'


        self.helper.layout = Layout(
            Div(
                Div(
                    Div('formador',css_class='col-sm-6'),
                    Div('nombre',css_class='col-sm-6'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_1',css_class='col-sm-2'),
                    Div('departamento_origen_1',css_class='col-sm-2'),
                    Div('municipio_origen_1',css_class='col-sm-2'),
                    Div('departamento_destino_1',css_class='col-sm-2'),
                    Div('municipio_destino_1',css_class='col-sm-2'),
                    Div('valor_1',css_class='col-sm-2'),
                    Div('id_1'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_2',css_class='col-sm-2'),
                    Div('departamento_origen_2',css_class='col-sm-2'),
                    Div('municipio_origen_2',css_class='col-sm-2'),
                    Div('departamento_destino_2',css_class='col-sm-2'),
                    Div('municipio_destino_2',css_class='col-sm-2'),
                    Div('valor_2',css_class='col-sm-2'),
                    Div('id_2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_3',css_class='col-sm-2'),
                    Div('departamento_origen_3',css_class='col-sm-2'),
                    Div('municipio_origen_3',css_class='col-sm-2'),
                    Div('departamento_destino_3',css_class='col-sm-2'),
                    Div('municipio_destino_3',css_class='col-sm-2'),
                    Div('valor_3',css_class='col-sm-2'),
                    Div('id_3'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_4',css_class='col-sm-2'),
                    Div('departamento_origen_4',css_class='col-sm-2'),
                    Div('municipio_origen_4',css_class='col-sm-2'),
                    Div('departamento_destino_4',css_class='col-sm-2'),
                    Div('municipio_destino_4',css_class='col-sm-2'),
                    Div('valor_4',css_class='col-sm-2'),
                    Div('id_4'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_5',css_class='col-sm-2'),
                    Div('departamento_origen_5',css_class='col-sm-2'),
                    Div('municipio_origen_5',css_class='col-sm-2'),
                    Div('departamento_destino_5',css_class='col-sm-2'),
                    Div('municipio_destino_5',css_class='col-sm-2'),
                    Div('valor_5',css_class='col-sm-2'),
                    Div('id_5'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_6',css_class='col-sm-2'),
                    Div('departamento_origen_6',css_class='col-sm-2'),
                    Div('municipio_origen_6',css_class='col-sm-2'),
                    Div('departamento_destino_6',css_class='col-sm-2'),
                    Div('municipio_destino_6',css_class='col-sm-2'),
                    Div('valor_6',css_class='col-sm-2'),
                    Div('id_6'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_7',css_class='col-sm-2'),
                    Div('departamento_origen_7',css_class='col-sm-2'),
                    Div('municipio_origen_7',css_class='col-sm-2'),
                    Div('departamento_destino_7',css_class='col-sm-2'),
                    Div('municipio_destino_7',css_class='col-sm-2'),
                    Div('valor_7',css_class='col-sm-2'),
                    Div('id_7'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_8',css_class='col-sm-2'),
                    Div('departamento_origen_8',css_class='col-sm-2'),
                    Div('municipio_origen_8',css_class='col-sm-2'),
                    Div('departamento_destino_8',css_class='col-sm-2'),
                    Div('municipio_destino_8',css_class='col-sm-2'),
                    Div('valor_8',css_class='col-sm-2'),
                    Div('id_8'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_9',css_class='col-sm-2'),
                    Div('departamento_origen_9',css_class='col-sm-2'),
                    Div('municipio_origen_9',css_class='col-sm-2'),
                    Div('departamento_destino_9',css_class='col-sm-2'),
                    Div('municipio_destino_9',css_class='col-sm-2'),
                    Div('valor_9',css_class='col-sm-2'),
                    Div('id_9'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_10',css_class='col-sm-2'),
                    Div('departamento_origen_10',css_class='col-sm-2'),
                    Div('municipio_origen_10',css_class='col-sm-2'),
                    Div('departamento_destino_10',css_class='col-sm-2'),
                    Div('municipio_destino_10',css_class='col-sm-2'),
                    Div('valor_10',css_class='col-sm-2'),
                    Div('id_10'),
                    css_class = 'row'
                ),

                css_class='text-center'
            )
        )