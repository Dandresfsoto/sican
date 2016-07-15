#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm
from django import forms
from usuarios.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML

class UserUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos personales',
                Div(
                    Div('first_name',css_class='col-sm-6'),
                    Div('last_name',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('telefono_personal',css_class='col-sm-6'),
                    Div('correo_personal',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),

            Fieldset(
                'Cuenta de usuario',
                Div(
                    HTML("""
                            <file-upload-sican style="margin-left:14px;" name="photo" old_file="{{photo_filename}}" link_old_file="{{photo_link}}">Foto</file-upload-sican>
                        """),
                    css_class = 'row'
                ),
                Div(
                    'photo',
                    css_class = 'hidden'
                ),
            ),
        )

    class Meta:
        model = User
        fields = ['first_name','last_name','telefono_personal','correo_personal','photo']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo corporativo',
        }

        widgets = {
            'email': forms.EmailInput(attrs={'readonly':True}),
            'cargo': forms.Select(attrs={'readonly':True})
        }