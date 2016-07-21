#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm, Form
from django import forms
from usuarios.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from permisos_sican.models import UserPermissionSican

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

class UserNewAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserNewAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos personales',
                Div(
                    Div('email',css_class='col-sm-12'),
                    css_class = 'row'
                ),
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
                    Div('cargo',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('groups',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('is_active',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = User
        fields = ['email','first_name','last_name','telefono_personal','correo_personal','cargo','is_active','groups']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'is_active': 'Activo',
        }
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'checked':''})
        }

class UserUpdateAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserUpdateAdminForm, self).__init__(*args, **kwargs)
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
                    Div('cargo',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('groups',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('is_active',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = User
        fields = ['first_name','last_name','telefono_personal','correo_personal','cargo','is_active','groups']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo corporativo',
            'is_active': 'Activo'
        }

        widgets = {
        }

class GroupNewAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupNewAdminForm, self).__init__(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(UserPermissionSican)
        exclude_perms = ['add_userpermissionsican','change_userpermissionsican','delete_userpermissionsican']
        self.fields['permissions'].queryset = Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información del grupo:',
                Div(
                    Div('name',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('permissions',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Group
        fields = '__all__'

        widget = {
        }

class ChangePasswordForm(Form):

    previus_password = forms.CharField(label='Contraseña anterior',max_length=100, widget=forms.PasswordInput())
    new_password_1 = forms.CharField(label='Nueva contraseña',max_length=100, widget=forms.PasswordInput())
    new_password_2 = forms.CharField(label='Repita la nueva contraseña',max_length=100, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.user = kwargs['initial']['user']
        self.helper.layout = Layout(
            Fieldset(
                'Cambio de contraseña:',
                Div(
                    Div('previus_password',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('new_password_1',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('new_password_2',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
        )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        previus_password = cleaned_data.get('previus_password')
        new_password_1 = cleaned_data.get('new_password_1')
        new_password_2 = cleaned_data.get('new_password_2')
        user = authenticate(email=self.user.email, password=previus_password)

        if user is None:
            self.add_error('previus_password','La contraseña no es correcta.')


        if new_password_1 != new_password_2:
            self.add_error('new_password_1',"Los campos de la nueva contraseña no coinciden.")
            self.add_error('new_password_2',"Los campos de la nueva contraseña no coinciden.")

class NuevoPermisoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NuevoPermisoForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].initial = ContentType.objects.get_for_model(UserPermissionSican)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información del permiso:',
                Div(
                    Div('name',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('codename',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('content_type',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
            ),
        )

    class Meta:
        model = Permission
        fields = '__all__'
        labels = {
            'codename': 'Codigo'
        }
        widget = {
        }
