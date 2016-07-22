from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from rh.models import TipoSoporte

class NuevoTipoSoporteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NuevoTipoSoporteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Tipo de soporte RH',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = TipoSoporte
        fields = '__all__'