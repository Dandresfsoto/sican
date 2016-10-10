from django.contrib import admin
from formadores.models import Formador
from formadores.models import SolicitudTransporte, Desplazamiento
from formadores.models import Producto, Revision, Cortes
from financiera.tasks import cortes

# Register your models here.

admin.site.register(Formador)
admin.site.register(SolicitudTransporte)
admin.site.register(Desplazamiento)
admin.site.register(Producto)
admin.site.register(Revision)


def cortes_archivo(modeladmin, request, queryset):
   for obj in queryset:
       cortes.delay(request.user.email,obj.id)
cortes_archivo.short_description = 'Actualizar archivo de corte'


class CortesAdmin(admin.ModelAdmin):
    list_display = ['descripcion']
    ordering = ['id']
    actions = [cortes_archivo]

admin.site.register(Cortes,CortesAdmin)