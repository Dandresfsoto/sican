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
from formadores.models import SolicitudTransporte
from informes.models import InformesExcel
from django.http import HttpResponse
from informes.tasks import formadores, formadores_soportes, preinscritos, transportes
from preinscripcion.models import DocentesPreinscritos
from encuestas.models import PercepcionInicial
from productos.models import Diplomado, Nivel, Sesion

# Create your views here.
class ResultadosPercepcionInicial(APIView):
    """
    Retorna los resultados de la encuesta de percepcion inicial.
    """
    def get(self, request, format=None):
        encuestas = PercepcionInicial.objects.all()

        response = {'0':encuestas.count(),
                    '1':{'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':0,'14':0,'15':0,},
                    '2':{'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0},
                    '3':{'si':0,'no':0},
                    '4':{'1':0,'2':0,'3':0,'4':0},
                    '5':{'1':0,'2':0,'3':0,'4':0},
                    '6':{'1':0,'2':0,'3':0,'4':0,'5':0},
                    '7':{'1':0,'2':0,'3':0,'4':0},
                    '8':{'1':0,'2':0,'3':0,'4':0},
                    '9':{'si':0,'no':0},
                    '10':{'1':0,'2':0,'3':0,'4':0},
                    '11':{'1':0,'2':0,'3':0,'4':0},
                    '12':{'si':0,'no':0},
                    '13':{'1':0,'2':0,'3':0,'4':0},
                    '14':{'si':0,'no':0},
                    '15':{'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0},
        }

        for encuesta in encuestas:
            response['1'][encuesta.area] += 1
            antiguedad = int(encuesta.antiguedad)

            if antiguedad > 0 and antiguedad <= 5:
                response['2']['1'] += 1
            if antiguedad > 5 and antiguedad <= 10:
                response['2']['2'] += 1
            if antiguedad > 10 and antiguedad <= 15:
                response['2']['3'] += 1
            if antiguedad > 15 and antiguedad <= 20:
                response['2']['4'] += 1
            if antiguedad > 20 and antiguedad <= 25:
                response['2']['5'] += 1
            if antiguedad > 25 and antiguedad <= 30:
                response['2']['6'] += 1
            if antiguedad > 30 and antiguedad <= 35:
                response['2']['7'] += 1
            if antiguedad > 35 and antiguedad <= 40:
                response['2']['8'] += 1
            if antiguedad > 40 and antiguedad <= 45:
                response['2']['9'] += 1
            if antiguedad > 45 and antiguedad <= 50:
                response['2']['10'] += 1

            if encuesta.pregunta_1 == 'Si':
                response['3']['si'] += 1
            else:
                response['3']['no'] += 1

            if encuesta.pregunta_2 != '':
                response['4'][encuesta.pregunta_2] += 1
            if encuesta.pregunta_3 != '':
                response['5'][encuesta.pregunta_3] += 1
            if encuesta.pregunta_4 != '':
                response['6'][encuesta.pregunta_4] += 1
            if encuesta.pregunta_5 != '':
                response['7'][encuesta.pregunta_5] += 1
            if encuesta.pregunta_6 != '':
                response['8'][encuesta.pregunta_6] += 1

            if encuesta.pregunta_7 != '':
                if encuesta.pregunta_7 == 'Si':
                    response['9']['si'] += 1
                else:
                    response['9']['no'] += 1
            if encuesta.pregunta_9 != '':
                response['10'][encuesta.pregunta_8] += 1
            if encuesta.pregunta_9 != '':
                response['11'][encuesta.pregunta_9] += 1
            if encuesta.pregunta_10 != '':
                if encuesta.pregunta_10 == 'Si':
                    response['12']['si'] += 1
                else:
                    response['12']['no'] += 1
            if encuesta.pregunta_11 != '':
                response['13'][encuesta.pregunta_11] += 1
            if encuesta.pregunta_12 != '':
                if encuesta.pregunta_12 == 'Si':
                    response['14']['si'] += 1
                else:
                    response['14']['no'] += 1

            if encuesta.pregunta_13 != '':
                escala = int(encuesta.pregunta_13)

                if escala > 0 and escala <= 10:
                    response['15']['1'] += 1
                if escala > 10 and escala <= 20:
                    response['15']['2'] += 1
                if escala > 20 and escala <= 30:
                    response['15']['3'] += 1
                if escala > 30 and escala <= 40:
                    response['15']['4'] += 1
                if escala > 40 and escala <= 50:
                    response['15']['5'] += 1
                if escala > 50 and escala <= 60:
                    response['15']['6'] += 1
                if escala > 60 and escala <= 70:
                    response['15']['7'] += 1
                if escala > 70 and escala <= 80:
                    response['15']['8'] += 1
                if escala > 80 and escala <= 90:
                    response['15']['9'] += 1
                if escala > 90 and escala <= 100:
                    response['15']['10'] += 1

        return Response(response)

class ReportesView(APIView):
    """
    Retorna la informacion de los usuarios excluyendo al que realiza el request.
    """
    def get(self, request, format=None):
        id_accion = request._request.GET['action']

        if id_accion == '1':
            x = formadores.delay(request.user.email)
        if id_accion == '2':
            x = formadores_soportes.delay(request.user.email)
        if id_accion == '3':
            x = preinscritos.delay(request.user.email)
        if id_accion == '4':
            x = transportes.delay(request.user.email)

        return HttpResponse(status=200)

class MunicipiosChainedList(APIView):
    """

    """

    permission_classes = (AllowAny,)

    def get(self, request, format=None):

        keys = [
            'departamento',
            'departamento_origen_1','departamento_destino_1',
            'departamento_origen_2','departamento_destino_2',
            'departamento_origen_3','departamento_destino_3',
            'departamento_origen_4','departamento_destino_4',
            'departamento_origen_5','departamento_destino_5',
            'departamento_origen_6','departamento_destino_6',
            'departamento_origen_7','departamento_destino_7',
            'departamento_origen_8','departamento_destino_8',
            'departamento_origen_9','departamento_destino_9',
            'departamento_origen_10','departamento_destino_10',

        ]

        for key in keys:
            if key in request._request.GET:
                id_departamento = request._request.GET[key]

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
            'financiera':{'name':'Financiera',
                  'icon':'icons:payment',
                  'id':'financiera',
                  'links':[]
            },
            'informes':{'name':'Mis informes',
                  'icon':'icons:assessment',
                  'id':'informes',
                  'links':[]
            },
            'formacion':{'name':'Formación',
                  'icon':'icons:language',
                  'id':'formacion',
                  'links':[]
            },
            'encuestas':{'name':'Encuestas',
                  'icon':'icons:assessment',
                  'id':'encuestas',
                  'links':[]
            },
        }

        links = {
            'transportesformacion':{
                'ver':{'name':'Solicitudes de transporte','link':'/formacion/transportes/'}
            },
            'sesiones':{
                'ver':{'name':'Sesiones','link':'/financiera/sesiones/'}
            },
            'niveles':{
                'ver':{'name':'Niveles','link':'/financiera/niveles/'}
            },
            'diplomados':{
                'ver':{'name':'Diplomados','link':'/financiera/diplomados/'}
            },
            'productos':{
                'ver':{'name':'Productos diplomados','link':'/financiera/productos/'}
            },
            'revision':{
                'ver':{'name':'Revisión documental','link':'/formacion/revision/'}
            },
            'percepcioninicial':{
                'ver':{'name':'Percepción inicial y detección de necesidades','link':'/encuestas/resultados/percepcioninicial/'}
            },
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
            'transportes':{
                'ver':{'name':'Solicitudes de transporte','link':'/financiera/transportes/'}
            },
            'excel':{
                'ver':{'name':'Informes en excel','link':'/informes/excel/'}
            },
            'preinscritos':{
                'ver':{'name':'Docentes preinscritos','link':'/formacion/preinscritos/'}
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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search) | Q(cedula__icontains=search)
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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

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
    max_display_length = 100

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

class SolicitudesTransporteList(BaseDatatableView):
    """
    0.formador
    1.cedula
    2.Lider
    3.id
    4.cantidad consignadas
    5.cantidad aprobadas financiera
    6.cantidad aprobadas lider
    7.cantidad rechazadas
    8.cantidad pendientes
    9.permiso para editar
    """
    model = Formador
    columns = ['nombres','cedula','lider','id']

    order_columns = ['nombres','cedula','lider','id']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | \
                Q(cedula__icontains=search) | Q(lider__first_name__icontains=search) | Q(lider__last_name__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            solicitudes = SolicitudTransporte.objects.filter(formador__cedula=item.cedula)
            json_data.append([
                item.get_full_name(),
                item.cedula,
                item.lider.get_full_name_string() if item.lider != None else '',
                item.id,
                solicitudes.filter(estado="consignado").count(),
                solicitudes.filter(estado="aprobado").count(),
                solicitudes.filter(estado="aprobado_lider").count(),
                solicitudes.filter(estado="rechazado").count(),
                solicitudes.filter(estado="revision").count(),
                self.request.user.has_perm('permisos_sican.financiera.transportes.editar'),
            ])
        return json_data

class InformesExcelList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.creacion
    3.archivo
    4.permiso para editar
    5.permiso para eliminar
    """
    model = InformesExcel
    columns = ['id','nombre','creacion','archivo']

    order_columns = ['id','nombre','creacion','archivo']
    max_display_length = 100

    def get_initial_queryset(self):
        return InformesExcel.objects.filter(usuario = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.creacion,
                item.get_archivo_url(),
                self.request.user.has_perm('permisos_sican.financiera.transportes.editar'),
                self.request.user.has_perm('permisos_sican.financiera.transportes.eliminar'),
            ])
        return json_data

class PreinscritosList(BaseDatatableView):
    """
    0.id
    1.primer apellido
    2.cargo
    3.departamento
    4.verificado
    5.cedula
    6.correo
    7.telefono_fijo
    8.telefono_celular
    9.radicado
    10.fecha
    11.permiso para editar
    12.permiso para eliminar
    """
    model = DocentesPreinscritos
    columns = ['id','primer_apellido','cargo','departamento','verificado']

    order_columns = ['id','primer_apellido','cargo','departamento','verificado']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(primer_apellido__icontains=search) | Q(segundo_apellido__icontains=search) |\
                Q(primer_nombre__icontains=search) | Q(segundo_nombre__icontains=search) |\
                Q(cargo__icontains=search) | Q(cargo__icontains=search) | Q(cedula__icontains=search) |\
                Q(departamento__nombre__icontains=search) | Q(municipio__nombre__icontains=search) |\
                Q(radicado__numero__icontains=search)

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.primer_apellido + ' ' + item.segundo_apellido + ' ' + item.primer_nombre + ' ' + item.segundo_nombre,
                item.cargo,
                item.departamento.nombre + ', ' + item.municipio.nombre,
                'Si' if item.verificado else 'No',
                item.cedula,
                item.correo,
                item.telefono_fijo,
                item.telefono_celular,
                item.radicado.numero,
                item.fecha,
                self.request.user.has_perm('permisos_sican.formacion.preinscritos.editar'),
                self.request.user.has_perm('permisos_sican.formacion.preinscritos.eliminar'),
            ])
        return json_data

class DiplomadosList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.permiso para editar
    4.permiso para eliminar
    """
    model = Diplomado
    columns = ['id','nombre','numero']

    order_columns = ['id','nombre','numero']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search) | Q(numero__icontains=search)

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                self.request.user.has_perm('permisos_sican.financiera.diplomados.editar'),
                self.request.user.has_perm('permisos_sican.financiera.diplomados.eliminar'),
            ])
        return json_data

class NivelesList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.diplomado
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Nivel
    columns = ['id','nombre','numero','diplomado']

    order_columns = ['id','nombre','numero','diplomado']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search) | Q(numero__icontains=search) | Q(diplomado__nombre__icontains=search)

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                item.diplomado.nombre,
                self.request.user.has_perm('permisos_sican.financiera.niveles.editar'),
                self.request.user.has_perm('permisos_sican.financiera.niveles.eliminar'),
            ])
        return json_data

class SesionesList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.diplomado
    4.nivel
    5.permiso para editar
    6.permiso para eliminar
    """
    model = Sesion
    columns = ['id','nombre','numero','diplomado','nivel']

    order_columns = ['id','nombre','numero','diplomado','nivel']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search) | Q(numero__icontains=search) | Q(nivel__nombre__icontains=search) | \
                Q(nivel__diplomado__nombre__icontains=search)

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                item.nivel.diplomado.nombre,
                item.nivel.nombre,
                self.request.user.has_perm('permisos_sican.financiera.sesiones.editar'),
                self.request.user.has_perm('permisos_sican.financiera.sesiones.eliminar'),
            ])
        return json_data

class SolicitudesTransporteFormacionList(BaseDatatableView):
    """
    0.id
    1.formador
    2.cedula
    3.cantidad aprobadas
    4.cantidad rechazadas
    5.cantidad pendientes
    6.permiso para editar
    """
    model = Formador
    columns = ['nombres','cedula','id']

    order_columns = ['nombres','cedula','id']
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.filter(lider = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | \
                Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            solicitudes = SolicitudTransporte.objects.filter(formador__cedula=item.cedula)
            json_data.append([
                item.get_full_name(),
                item.cedula,
                item.id,
                solicitudes.filter(estado="aprobado_lider").count(),
                solicitudes.filter(estado="rechazado").count(),
                solicitudes.filter(estado="revision").count(),
                self.request.user.has_perm('permisos_sican.financiera.transportes.editar'),
            ])
        return json_data

class SolicitudesTransporteFormadorList(BaseDatatableView):
    """
    0.id
    1.formador
    2.fecha
    3.valor
    4.valor_aprobado_lider
    5.valor_aprobado
    6.desplazamientos
    7.estado
    8.archivo
    9.nombre
    10.permiso para editar
    11.permiso para eliminar
    12.permiso para cambiar estado
    """
    model = SolicitudTransporte
    columns = ['id','nombre','creacion','valor','valor_aprobado_lider','valor_aprobado','estado']

    order_columns = ['id','nombre','creacion','valor','valor_aprobado_lider','valor_aprobado','estado']
    max_display_length = 100

    def get_initial_queryset(self):
        estado = self.request.GET['estado']
        return SolicitudTransporte.objects.filter(formador__id=self.kwargs['id_formador']).filter(estado=estado)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(formador__nombres__icontains=search) | Q(formador__apellidos__icontains=search) | \
                Q(formador__cedula__icontains=search) | Q(estado__icontains=search.lower())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            formador = item.formador.nombres + " " + item.formador.apellidos

            desplazamientos_response = []

            for desplazamiento in item.desplazamientos.all():
                desplazamientos_response.append([
                    desplazamiento.fecha,
                    desplazamiento.departamento_origen.nombre,
                    desplazamiento.municipio_origen.nombre,
                    desplazamiento.departamento_destino.nombre,
                    desplazamiento.municipio_destino.nombre,
                    desplazamiento.valor,
                    desplazamiento.motivo
                ])

            json_data.append([
                item.id,
                formador,
                item.creacion,
                item.valor,
                item.valor_aprobado_lider,
                item.valor_aprobado,
                desplazamientos_response,
                item.estado,
                item.get_archivo_url(),
                item.nombre,
                self.request.user.has_perm('permisos_sican.formacion.transportesformacion.editar'),
                self.request.user.has_perm('permisos_sican.formacion.transportesformacion.eliminar'),
                self.request.user.has_perm('permisos_sican.formacion.transportesformacion.estado'),
            ])
        return json_data

class SolicitudesTransporteFormadorFinancieraList(BaseDatatableView):
    """
    0.id
    1.formador
    2.fecha
    3.valor
    4.valor_aprobado_lider
    5.valor_aprobado
    6.desplazamientos
    7.estado
    8.archivo
    9.nombre
    10.permiso para editar
    11.permiso para eliminar
    12.permiso para cambiar estado
    """
    model = SolicitudTransporte
    columns = ['id','nombre','creacion','valor','valor_aprobado_lider','valor_aprobado','estado']

    order_columns = ['id','nombre','creacion','valor','valor_aprobado_lider','valor_aprobado','estado']
    max_display_length = 100

    def get_initial_queryset(self):
        estado = self.request.GET['estado']
        return SolicitudTransporte.objects.filter(formador__id=self.kwargs['id_formador']).filter(estado=estado)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(formador__nombres__icontains=search) | Q(formador__apellidos__icontains=search) | \
                Q(formador__cedula__icontains=search) | Q(estado__icontains=search.lower())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            formador = item.formador.nombres + " " + item.formador.apellidos

            desplazamientos_response = []

            for desplazamiento in item.desplazamientos.all():
                desplazamientos_response.append([
                    desplazamiento.fecha,
                    desplazamiento.departamento_origen.nombre,
                    desplazamiento.municipio_origen.nombre,
                    desplazamiento.departamento_destino.nombre,
                    desplazamiento.municipio_destino.nombre,
                    desplazamiento.valor,
                    desplazamiento.motivo
                ])

            json_data.append([
                item.id,
                formador,
                item.creacion,
                item.valor,
                item.valor_aprobado_lider,
                item.valor_aprobado,
                desplazamientos_response,
                item.estado,
                item.get_archivo_url(),
                item.nombre,
                self.request.user.has_perm('permisos_sican.financiera.transportes.editar'),
                self.request.user.has_perm('permisos_sican.financiera.transportes.eliminar'),
                self.request.user.has_perm('permisos_sican.financiera.transportes.estado'),
            ])
        return json_data