#!/usr/bin/env python
# -*- coding: utf-8 -*-
from usuarios.models import User
from rest.serializers import UserSerializer, MensajeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from inbox.models import Mensaje
from django_datatables_view.base_datatable_view import BaseDatatableView
from administrativos.models import Administrativo, Soporte
from cargos.models import Cargo
from django.db.models import Q
from usuarios.models import User
from permisos_sican.models import UserPermissionSican
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rh.models import TipoSoporte
from operator import itemgetter
from formadores.models import Formador
from formadores.models import Soporte as SoporteFormador
from departamentos.models import Departamento
from municipios.models import Municipio
from secretarias.models import Secretaria
from radicados.models import Radicado
from rest_framework.permissions import AllowAny

# Create your views here.

class MunicipiosChainedList(APIView):
    """

    """

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        id_departamento = request._request.GET['departamento']
        if id_departamento == '':
            id_departamento = 0
        municipios = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

        response = {}

        for municipio in municipios:
            response[municipio[0]] = municipio[1]

        return Response(response)

class RadicadosChainedList(APIView):
    """

    """
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        try:
            id_municipio = request._request.GET['municipio']
        except:
            id_municipio = 0
        if id_municipio == '':
            id_municipio = 0
        radicados = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        response = {}

        for radicado in radicados:
            response[radicado[0]] = radicado[1]

        return Response(response)

class UserList(APIView):
    """
    Retorna la informacion de los usuarios excluyendo al que realiza el request.
    """
    def get(self, request, format=None):
        users = User.objects.exclude(id = request.user.id).exclude(email="AnonymousUser")
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

class UserChatList(APIView):
    def get(self, request, format=None):
        users = Mensaje.objects.exclude(user = request.user)
        serializer = MensajeSerializer(users,many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    def get(request, *args, **kwargs):
        users = User.objects.filter(id=kwargs['id'])
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

class UserPermissionList(APIView):
    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        perms_user = list(user.get_all_permissions())

        categories = {
            'adminuser':{'name':'Usuarios',
                  'icon':'icons:account-circle',
                  'id':'usuarios',
                  'links':[]
            },
            'rh':{'name':'Recursos Humanos',
                  'icon':'icons:accessibility',
                  'id':'rh',
                  'links':[]
            },
            'bases':{'name':'Bases de datos',
                  'icon':'icons:dashboard',
                  'id':'bases',
                  'links':[]
            },
        }

        links = {
            'permisos':{
                'ver':{'name':'Permisos','link':'/adminuser/permisos/'}
            },
            'usuarios':{
                'ver':{'name':'Usuarios','link':'/adminuser/usuarios/'}
            },
            'grupos':{
                'ver':{'name':'Grupos','link':'/adminuser/grupos/'}
            },
            'administrativos':{
                'ver':{'name':'Administrativos','link':'/rh/administrativos/'}
            },
            'cargos':{
                'ver':{'name':'Cargos','link':'/rh/cargos/'}
            },
            'rh_tipo_soporte':{
                'ver':{'name':'Tipo de soportes','link':'/rh/tipo_soporte/'}
            },
            'formadores':{
                'ver':{'name':'Formadores','link':'/rh/formadores/'}
            },
            'departamentos':{
                'ver':{'name':'Departamentos','link':'/bases/departamentos/'}
            },
            'municipios':{
                'ver':{'name':'Municipios','link':'/bases/municipios/'}
            },
            'secretarias':{
                'ver':{'name':'Secretarias de educación','link':'/bases/secretarias/'}
            },
            'radicados':{
                'ver':{'name':'Radicados','link':'/bases/radicados/'}
            },
        }




        perms_response = []
        perms_dict = {}

        content_type = ContentType.objects.get_for_model(UserPermissionSican)
        exclude_perms = ['add_userpermissionsican','change_userpermissionsican','delete_userpermissionsican']
        permissions = Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms).values_list('codename',flat=True)
        app = 'permisos_sican.'

        array_tuple = []

        for perm_user in perms_user:

            if perm_user.replace(app,'') in permissions:
                category, links_group, link = perm_user.replace(app,'').split('.')
                if links_group in links:
                    if link in links[links_group]:
                        array_tuple.append(([category,links_group,link],categories[category]['name'],links[links_group][link]['name']))
                        array_tuple.sort(key=itemgetter(1,2))

        for perm in array_tuple:
            perms_dict[perm[0][0]] = categories[perm[0][0]]
            perms_dict[perm[0][0]]['links'].append(links[perm[0][1]][perm[0][2]])


        for key, value in perms_dict.iteritems():
            perms_response.append((key,value,categories[key]['name']))
            perms_response.sort(key=itemgetter(2))

        r = []

        for res in perms_response:
            r.append(res[1])




        return Response(r)

class AdministrativosRh(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.correo_personal
    6.celular_personal
    7.profesion
    8.correo_corporativo
    9.celular_corporativo
    10.fecha_contratacion
    11.fecha_terminacion
    12.banco
    13.tipo_cuenta
    14.numero_cuenta
    15.eps
    16.pension
    17.arl
    18.permiso para editar
    19.permiso para eliminar
    20.permiso para ver soportes
    """
    model = Administrativo
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'correo_corporativo','celular_corporativo','fecha_contratacion','fecha_terminacion',
               'banco','tipo_cuenta','numero_cuenta','eps','pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 10

    def get_initial_queryset(self):
        return Administrativo.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:

            region_str = ''
            for region in item.region.values_list('numero',flat=True):
                region_str = region_str + str(region) + ','
            region_str = region_str[:-1]

            if item.banco != None:
                banco = item.banco.nombre
            else:
                banco = ''

            json_data.append([
                item.id,
                item.nombres + " " + item.apellidos,
                item.cargo.nombre,
                region_str,
                item.cedula,
                item.correo_personal,
                item.celular_personal,
                item.profesion,
                item.correo_corporativo,
                item.celular_corporativo,
                item.fecha_contratacion,
                item.fecha_terminacion,
                banco,
                item.tipo_cuenta,
                item.numero_cuenta,
                item.eps,
                item.pension,
                item.arl,
                self.request.user.has_perm('permisos_sican.rh.administrativos.editar'),
                self.request.user.has_perm('permisos_sican.rh.administrativos.eliminar'),
                self.request.user.has_perm('permisos_sican.rh.administrativos_soportes.ver'),
            ])
        return json_data

class CargosRh(BaseDatatableView):
    """
    0.id
    1.nombre
    2.manual (retorna la url o string vacio)
    3.descripcion
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Cargo
    columns = ['id','nombre','manual','descripcion']

    order_columns = ['','nombre','']
    max_display_length = 10

    def get_initial_queryset(self):
        return Cargo.objects.filter(oculto = False)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            try:
                url = item.manual.url
            except:
                url = ""

            json_data.append([
                item.id,
                item.nombre,
                url,
                item.descripcion,
                self.request.user.has_perm('permisos_sican.rh.cargos.editar'),
                self.request.user.has_perm('permisos_sican.rh.cargos.eliminar'),
            ])
        return json_data

class AdministrativosRhSoportes(BaseDatatableView):
    """
    0.id
    1.tipo
    2.fecha
    3.descripcion
    4.archivo (url o string vacio)
    5.creacion
    6.permiso para editar
    7.permiso para eliminar
    """
    model = Soporte
    columns = ['id','tipo','fecha','descripcion','get_archivo_url','creacion']

    order_columns = ['id','tipo','fecha','descripcion']
    max_display_length = 10

    def get_initial_queryset(self):
        return Soporte.objects.filter(oculto = False,administrativo__id=self.kwargs['id_administrativo'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(tipo__nombre__icontains=search) | Q(tipo__descripcion__icontains=search) | Q(fecha__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.tipo.nombre,
                item.fecha,
                item.tipo.descripcion,
                item.get_archivo_url(),
                item.creacion,
                self.request.user.has_perm('permisos_sican.rh.administrativos_soportes.editar'),
                self.request.user.has_perm('permisos_sican.rh.administrativos_soportes.eliminar'),
            ])
        return json_data

class AdminUserList(BaseDatatableView):
    """
    0.id
    1.email
    2.first_name
    3.last_name
    4.is_active
    5.cargo
    6.telefono_personal
    7.correo_personal
    8.permiso para editar
    """
    model = User
    columns = ['id','email','first_name','last_name','is_active','cargo','telefono_personal','correo_personal']

    order_columns = ['id','email','first_name','last_name']
    max_display_length = 10

    def get_initial_queryset(self):
        return User.objects.exclude(email="AnonymousUser")


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.email,
                item.first_name,
                item.last_name,
                item.is_active,
                item.cargo.nombre,
                item.telefono_personal,
                item.correo_personal,
                self.request.user.has_perm('permisos_sican.adminuser.usuarios.editar'),
            ])
        return json_data

class GroupUserList(BaseDatatableView):
    """
    0.id
    1.name
    2.permissions
    3.permiso para editar
    4.permiso para eliminar
    """
    model = Group
    columns = ['id','name','permissions']

    order_columns = ['id','name']
    max_display_length = 10

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(name__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            result = []
            permisos = Group.objects.get(id=item.id).permissions.all()
            for permiso in permisos:
                result.append(permiso.__str__())
            json_data.append([
                item.id,
                item.name,
                result,
                self.request.user.has_perm('permisos_sican.adminuser.grupos.editar'),
                self.request.user.has_perm('permisos_sican.adminuser.grupos.eliminar'),
            ])
        return json_data

class AdminUserPermissionList(BaseDatatableView):
    """
    0.id
    1.name
    2.codename
    3.permiso para editar
    4.permiso para eliminar
    """
    model = Permission
    columns = ['id','name','codename']
    order_columns = ['id','name','codename']
    max_display_length = 10

    def get_initial_queryset(self):
        content_type = ContentType.objects.get_for_model(UserPermissionSican)
        exclude_perms = ['add_userpermissionsican','change_userpermissionsican','delete_userpermissionsican']
        return Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.name,
                item.codename,
                self.request.user.has_perm('permisos_sican.adminuser.permisos.editar'),
                self.request.user.has_perm('permisos_sican.adminuser.permisos.eliminar')
            ])
        return json_data

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(codename__icontains=search) | Q(name__icontains=search)
            qs = qs.filter(q)
        return qs

class TipoSoporteRh(BaseDatatableView):
    """
    0.id
    1.nombre
    2.descripcion
    3.permiso para editar
    4.permiso para eliminar
    """
    model = TipoSoporte
    columns = ['id','nombre','descripcion']
    order_columns = ['id','nombre','descripcion']
    max_display_length = 10

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.descripcion,
                self.request.user.has_perm('permisos_sican.rh.rh_tipo_soporte.crear'),
                self.request.user.has_perm('permisos_sican.rh.rh_tipo_soporte.eliminar')
            ])
        return json_data

    def get_initial_queryset(self):
        return TipoSoporte.objects.exclude(oculto = True)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search) | Q(descripcion__icontains=search)
            qs = qs.filter(q)
        return qs

class FormadoresRh(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.correo_personal
    6.celular_personal
    7.profesion
    8.fecha_contratacion
    9.fecha_terminacion
    10.banco
    11.tipo_cuenta
    12.numero_cuenta
    13.eps
    14.pension
    15.arl
    16.permiso para editar
    17.permiso para eliminar
    18.permiso para ver soportes
    """
    model = Formador
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'fecha_contratacion','fecha_terminacion','banco','tipo_cuenta','numero_cuenta','eps',
               'pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 10

    def get_initial_queryset(self):
        return Formador.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:

            region_str = ''
            for region in item.region.values_list('numero',flat=True):
                region_str = region_str + str(region) + ','
            region_str = region_str[:-1]

            if item.banco != None:
                banco = item.banco.nombre
            else:
                banco = ''

            json_data.append([
                item.id,
                item.nombres + " " + item.apellidos,
                item.cargo.nombre,
                region_str,
                item.cedula,
                item.correo_personal,
                item.celular_personal,
                item.profesion,
                item.fecha_contratacion,
                item.fecha_terminacion,
                banco,
                item.tipo_cuenta,
                item.numero_cuenta,
                item.eps,
                item.pension,
                item.arl,
                self.request.user.has_perm('permisos_sican.rh.formadores.editar'),
                self.request.user.has_perm('permisos_sican.rh.formadores.eliminar'),
                self.request.user.has_perm('permisos_sican.rh.formadores_soportes.ver'),
            ])
        return json_data

class FormadoresRhSoportes(BaseDatatableView):
    """
    0.id
    1.tipo
    2.fecha
    3.descripcion
    4.archivo (url o string vacio)
    5.creacion
    6.permiso para editar
    7.permiso para eliminar
    """
    model = SoporteFormador
    columns = ['id','tipo','fecha','descripcion','get_archivo_url','creacion']

    order_columns = ['id','tipo','fecha','descripcion']
    max_display_length = 10

    def get_initial_queryset(self):
        return SoporteFormador.objects.filter(oculto = False,formador__id=self.kwargs['id_formador'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(tipo__nombre__icontains=search) | Q(tipo__descripcion__icontains=search) | Q(fecha__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.tipo.nombre,
                item.fecha,
                item.tipo.descripcion,
                item.get_archivo_url(),
                item.creacion,
                self.request.user.has_perm('permisos_sican.rh.formadores_soportes.editar'),
                self.request.user.has_perm('permisos_sican.rh.formadores_soportes.eliminar'),
            ])
        return json_data

class DepartamentosList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.codigo_departamento
    3.codigo_auditoria
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Departamento
    columns = ['id','nombre','codigo_departamento']

    order_columns = ['id','nombre','codigo_departamento']
    max_display_length = 10

    def get_initial_queryset(self):
        return Departamento.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search) | Q(codigo_departamento__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.codigo_departamento,
                item.codigo_auditoria,
                self.request.user.has_perm('permisos_sican.bases.departamentos.editar'),
                self.request.user.has_perm('permisos_sican.bases.departamentos.eliminar'),
            ])
        return json_data

class MunicipiosList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.departamento
    3.codigo_municipio
    4.codigo_auditoria
    5.permiso para editar
    6.permiso para eliminar
    """
    model = Municipio
    columns = ['id','nombre','departamento','codigo_municipio','codigo_auditoria']

    order_columns = ['id','nombre','departamento','codigo_municipio','codigo_auditoria']
    max_display_length = 10

    def get_initial_queryset(self):
        return Municipio.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(departamento__nombre__icontains=search) | Q(nombre__icontains=search) | Q(codigo_municipio__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.departamento.nombre,
                item.codigo_municipio,
                item.codigo_auditoria,
                self.request.user.has_perm('permisos_sican.bases.municipios.editar'),
                self.request.user.has_perm('permisos_sican.bases.municipios.eliminar'),
            ])
        return json_data

class SecretariasList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.departamento
    3.tipo
    4.direccion
    5.web
    6.permiso para editar
    7.permiso para eliminar
    """
    model = Secretaria
    columns = ['id','nombre','municipio','tipo','direccion','web']

    order_columns = ['id','nombre','municipio','tipo','direccion','web']
    max_display_length = 10

    def get_initial_queryset(self):
        return Secretaria.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(municipio__departamento__nombre__icontains=search) | Q(municipio__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.municipio.departamento.nombre,
                item.tipo,
                item.direccion,
                item.web,
                self.request.user.has_perm('permisos_sican.bases.secretarias.editar'),
                self.request.user.has_perm('permisos_sican.bases.secretarias.eliminar'),
            ])
        return json_data

class RadicadosList(BaseDatatableView):
    """
    0.id
    1.numero
    2.secretaria
    3.municipio
    4.nombre_sede

    5.dane_sede
    6.tipo
    7.ubicacion
    8.permiso para editar
    9.permiso para eliminar
    """
    model = Secretaria
    columns = ['id','numero','secretaria','municipio','nombre_sede','dane_sede','tipo','ubicacion']

    order_columns = ['id','numero','secretaria','municipio','nombre_sede','dane_sede','tipo','ubicacion']
    max_display_length = 10

    def get_initial_queryset(self):
        return Radicado.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(numero__icontains=search) | Q(secretaria__nombre__icontains=search) | \
                Q(municipio__nombre__icontains=search) | Q(municipio__departamento__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.numero,
                item.secretaria.nombre,
                item.municipio.nombre,
                item.nombre_sede,
                item.dane_sede,
                item.tipo,
                item.ubicacion,
                self.request.user.has_perm('permisos_sican.bases.radicados.editar'),
                self.request.user.has_perm('permisos_sican.bases.radicados.eliminar'),
            ])
        return json_data