#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML, Submit, ButtonHolder
from rh.models import TipoSoporte, RequerimientoPersonal
from usuarios.models import User
from municipios.models import Municipio

class ConsultaBeneficiarioForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ConsultaBeneficiarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div('cedula',css_class='col-sm-offset-4 col-sm-4'),
                css_class = 'row'
            ),
            HTML("""
                <button type="submit" class="btn btn-cpe">Consultar</button>
            """)
        )
    cedula = forms.CharField(max_length=100,label='Digita tu numero de cédula (sin puntos o comas)')