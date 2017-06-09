#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from beneficiarios.models import GruposBeneficiarios
from beneficiarios.models import Contrato


class GruposBeneficiariosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GruposBeneficiariosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['numero'].initial = GruposBeneficiarios.objects.filter(usuario = kwargs['initial']['user']).count() + 1
        self.fields['usuario'].initial = kwargs['initial']['user']
        self.fields['contrato'].queryset = Contrato.objects.filter(formador__usuario = kwargs['initial']['user'])

        self.helper.layout = Layout(
            Fieldset(
                'Selección de contrato',
                Div(
                    Div('contrato',css_class='col-sm-12'),
                    HTML(
                        """
                        <div class="col-sm-12">
                            <div>
                                <p class="inline"><b>Vigencia:</b></p><p class="inline" id="p_vigencia"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Municipios:</b></p><p class="inline" id="p_municipios"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Supervisores:</b></p><p class="inline" id="p_supervisores"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Meta de beneficiarios:</b></p><p class="inline" id="p_meta_beneficiarios"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Inscritos en contrato:</b></p><p class="inline" id="p_inscritos_contrato"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Inscritos en grupo:</b></p><p class="inline" id="p_inscritos_grupo"> ---- </p>
                            </div>
                        </div>
                        """
                    ),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Información del grupo',
                Div(
                    Div('nombre',css_class='col-sm-6'),
                    Div('diplomado_grupo',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    'numero',css_class='hidden'
                ),
                Div(
                    'usuario',css_class='hidden'
                ),
            )
        )

    class Meta:
        model = GruposBeneficiarios
        fields = '__all__'
        labels = {
            'diplomado_grupo': 'Diplomado',
            'descripcion': 'Descripción',
        }
        widgets = {
            'descripcion': forms.Textarea(),
        }