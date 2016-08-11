from django.contrib import admin
from formadores.models import Formador
from formadores.models import SolicitudTransporte, Desplazamiento
# Register your models here.

admin.site.register(Formador)
admin.site.register(SolicitudTransporte)
admin.site.register(Desplazamiento)