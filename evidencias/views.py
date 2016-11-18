#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from productos.models import Diplomado, Nivel, Sesion
from formadores.models import Formador
from evidencias.models import Evidencia
from evidencias.forms import EvidenciaForm
from productos.models import Entregable
from evidencias.models import Red
from evidencias.forms import RedForm, RedRetroalimentacionForm
from region.models import Region
from django.shortcuts import HttpResponseRedirect
from evidencias.tasks import build_red, carga_masiva_evidencias, retroalimentacion_red
from evidencias.models import CargaMasiva
from evidencias.forms import CargaMasivaForm

# Create your views here.

class DiplomadosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_diplomados.html'
    permission_required = "permisos_sican.evidencias.general.ver"



class FormadoresListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_formadores.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.evidencias.general.informes')
        return super(FormadoresListView,self).get_context_data(**kwargs)



class NivelesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_niveles.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.evidencias.general.informes')
        return super(NivelesListView,self).get_context_data(**kwargs)



class SesionesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_sesiones.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        return super(SesionesListView,self).get_context_data(**kwargs)


class EntregablesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_entregables.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        return super(EntregablesListView,self).get_context_data(**kwargs)



class SoportesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_soportes.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(SoportesListView,self).get_context_data(**kwargs)


class NuevoSoporteView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Evidencia
    form_class = EvidenciaForm
    success_url = '../'
    template_name = 'evidencias/general/nuevo.html'
    permission_required = "permisos_sican.evidencias.general.crear"

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador'],'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(NuevoSoporteView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        cargados = self.object.beneficiarios_cargados.all()
        formador = Formador.objects.get(id = self.kwargs['id_formador'])
        entregable = Entregable.objects.get(id = self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(formador = formador,entregable = entregable).filter(beneficiarios_cargados__id__in = cargados.values_list('id',flat=True))

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)

        return super(NuevoSoporteView,self).form_valid(form)


class UpdateSoporteView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Evidencia
    form_class = EvidenciaForm
    success_url = '../../'
    pk_url_kwarg = 'id_soporte'
    template_name = 'evidencias/general/nuevo.html'
    permission_required = "permisos_sican.evidencias.general.editar"

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador'],'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(UpdateSoporteView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        cargados = self.object.beneficiarios_cargados.all()
        formador = Formador.objects.get(id = self.kwargs['id_formador'])
        entregable = Entregable.objects.get(id = self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(formador = formador,entregable = entregable).filter(beneficiarios_cargados__id__in = cargados.values_list('id',flat=True))

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)

        return super(UpdateSoporteView,self).form_valid(form)


class DeleteSoporteView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Evidencia
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'evidencias/general/eliminar.html'
    permission_required = "permisos_sican.evidencias.general.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(DeleteSoporteView,self).get_context_data(**kwargs)



class EvidenciasListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/codigos/lista.html'
    permission_required = "permisos_sican.evidencias.codigos.ver"

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.evidencias.codigos.informes')
        return super(EvidenciasListView,self).get_context_data(**kwargs)


class RedsListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/red/lista.html'
    permission_required = "permisos_sican.evidencias.red.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.red.crear')
        return super(RedsListView,self).get_context_data(**kwargs)


class NuevoRedView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Red
    form_class = RedForm
    success_url = '../'
    template_name = 'evidencias/red/nuevo.html'
    permission_required = "permisos_sican.evidencias.red.crear"

    def get_context_data(self, **kwargs):

        evidencias_red_list = Red.objects.all().values_list('evidencias__id',flat=True)
        evidencias = Evidencia.objects.exclude(id__in = evidencias_red_list)

        region_1 = Region.objects.get(numero = 1)
        region_2 = Region.objects.get(numero = 2)

        evidencias_r1 = evidencias.filter(formador__region = region_1)
        evidencias_r2 = evidencias.filter(formador__region = region_2)

        evidencias_r1_innovatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
        evidencias_r1_tecnotic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
        evidencias_r1_directic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
        evidencias_r1_escuelatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')

        evidencias_r2_innovatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
        evidencias_r2_tecnotic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
        evidencias_r2_directic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
        evidencias_r2_escuelatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')


        kwargs['formadores_innovatic_r1'] = evidencias_r1_innovatic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_innovatic_r1'] = evidencias_r1_innovatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_innovatic_r1'] = evidencias_r1_innovatic.count()

        kwargs['formadores_tecnotic_r1'] = evidencias_r1_tecnotic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_tecnotic_r1'] = evidencias_r1_tecnotic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_tecnotic_r1'] = evidencias_r1_tecnotic.count()

        kwargs['formadores_directic_r1'] = evidencias_r1_directic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_directic_r1'] = evidencias_r1_directic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_directic_r1'] = evidencias_r1_directic.count()

        kwargs['formadores_escuelatic_r1'] = evidencias_r1_escuelatic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_escuelatic_r1'] = evidencias_r1_escuelatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_escuelatic_r1'] = evidencias_r1_escuelatic.count()

        kwargs['formadores_innovatic_r2'] = evidencias_r2_innovatic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_innovatic_r2'] = evidencias_r2_innovatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_innovatic_r2'] = evidencias_r2_innovatic.count()

        kwargs['formadores_tecnotic_r2'] = evidencias_r2_tecnotic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_tecnotic_r2'] = evidencias_r2_tecnotic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_tecnotic_r2'] = evidencias_r2_tecnotic.count()

        kwargs['formadores_directic_r2'] = evidencias_r2_directic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_directic_r2'] = evidencias_r2_directic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_directic_r2'] = evidencias_r2_directic.count()

        kwargs['formadores_escuelatic_r2'] = evidencias_r2_escuelatic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_escuelatic_r2'] = evidencias_r2_escuelatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_escuelatic_r2'] = evidencias_r2_escuelatic.count()

        return super(NuevoRedView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        evidencias_red_list = Red.objects.all().exclude(evidencias = None).values_list('evidencias__id',flat=True)
        evidencias = Evidencia.objects.exclude(id__in = evidencias_red_list)

        region_1 = Region.objects.get(numero = 1)
        region_2 = Region.objects.get(numero = 2)

        evidencias_r1 = evidencias.filter(formador__region = region_1)
        evidencias_r2 = evidencias.filter(formador__region = region_2)

        evidencias_r1_innovatic = list(evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC'))
        evidencias_r1_tecnotic = list(evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC'))
        evidencias_r1_directic = list(evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC'))
        evidencias_r1_escuelatic = list(evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA'))

        evidencias_r2_innovatic = list(evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC'))
        evidencias_r2_tecnotic = list(evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC'))
        evidencias_r2_directic = list(evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC'))
        evidencias_r2_escuelatic = list(evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA'))

        red = Red.objects.get(id = self.object.id)

        if self.object.region.numero == 1:
            if self.object.diplomado.nombre == 'INNOVATIC':
                red.evidencias.add(*evidencias_r1_innovatic)
            elif self.object.diplomado.nombre == 'TECNOTIC':
                red.evidencias.add(*evidencias_r1_tecnotic)
            elif self.object.diplomado.nombre == 'DIRECTIC':
                red.evidencias.add(*evidencias_r1_directic)
            elif self.object.diplomado.nombre == 'ESCUELA TIC FAMILIA':
                red.evidencias.add(*evidencias_r1_escuelatic)
            else:
                pass

        elif self.object.region.numero == 2:
            if self.object.diplomado.nombre == 'INNOVATIC':
                red.evidencias.add(*evidencias_r2_innovatic)
            elif self.object.diplomado.nombre == 'TECNOTIC':
                red.evidencias.add(*evidencias_r2_tecnotic)
            elif self.object.diplomado.nombre == 'DIRECTIC':
                red.evidencias.add(*evidencias_r2_directic)
            elif self.object.diplomado.nombre == 'ESCUELA TIC FAMILIA':
                red.evidencias.add(*evidencias_r2_escuelatic)
            else:
                pass


        else:
            pass
        red.save()
        build_red.delay(red.id)
        return HttpResponseRedirect(self.get_success_url())


class UpdateRedView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Red
    form_class = RedRetroalimentacionForm
    success_url = '../../'
    template_name = 'evidencias/red/editar.html'
    permission_required = "permisos_sican.evidencias.red.editar"


    def form_valid(self, form):
        self.object = form.save()
        retroalimentacion_red.delay(self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class CargaMasivaListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/cargamasiva/lista.html'
    permission_required = "permisos_sican.evidencias.cargamasivaevidencias.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.cargamasivaevidencias.crear')
        return super(CargaMasivaListView,self).get_context_data(**kwargs)


class NuevoCargaMasivaView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = CargaMasiva
    form_class = CargaMasivaForm
    success_url = '../'
    template_name = 'evidencias/cargamasiva/nuevo.html'
    permission_required = "permisos_sican.evidencias.cargamasivaevidencias.crear"

    def get_initial(self):
        return {'id_usuario':self.request.user.id}

    def form_valid(self, form):
        self.object = form.save()
        carga_masiva_evidencias.delay(self.object.id,self.request.user.id)
        return super(NuevoCargaMasivaView,self).form_valid(form)

class AuxiliaresListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/rendimiento/lista.html'
    permission_required = "permisos_sican.auxiliares.rendimiento.ver"