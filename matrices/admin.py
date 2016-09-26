from django.contrib import admin
from matrices.models import Area, Grado, Beneficiario
from matrices.models import CargaMasiva
# Register your models here.

admin.site.register(Area)
admin.site.register(Grado)
admin.site.register(Beneficiario)
admin.site.register(CargaMasiva)