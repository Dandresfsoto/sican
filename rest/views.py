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

# Create your views here.

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
            'rh':{'name':'Recursos Humanos',
                  'icon':'icons:accessibility',
                  'id':'rh',
                  'links':[
                      {'name':'Administrativos','link':'/rh/administrativos/'},
                      {'name':'Cargos','link':'/rh/cargos/'}
                  ]
            },
            'adminuser':{'name':'Administración de usuarios',
                  'icon':'icons:account-circle',
                  'id':'usuarios',
                  'links':[]
            },
        }

        links = {
            'permisos':{
                'ver':{'name':'Permisos de usuario','link':'/adminuser/permisos/'}
            },
            'usuarios':{
                'ver':{'name':'Usuarios','link':'/adminuser/usuarios/'}
            },
            'grupos':{
                'ver':{'name':'Grupos de usuarios','link':'/adminuser/grupos/'}
            }
        }


        perms_response = []
        perms_dict = {}

        content_type = ContentType.objects.get_for_model(UserPermissionSican)
        exclude_perms = ['add_userpermissionsican','change_userpermissionsican','delete_userpermissionsican']
        permissions = Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms).values_list('codename',flat=True)
        app = 'permisos_sican.'

        for perm_user in perms_user:

            if perm_user.replace(app,'') in permissions:
                category, links_group, link = perm_user.replace(app,'').split('.')
                if links_group in links:
                    if link in links[links_group]:
                        perms_dict[category] = categories[category]
                        perms_dict[category]['links'].append(links[links_group][link])


        for key, value in perms_dict.iteritems():
            perms_response.append(value)



        return Response(perms_response)

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
    """
    model = Administrativo
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'correo_corporativo','celular_corporativo','fecha_contratacion','fecha_terminacion',
               'banco','tipo_cuenta','numero_cuenta','eps','pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 10

    def get_initial_queryset(self):
        return Administrativo.objects.filter(oculto = False)

    def render_column(self, row, column):
        if column == 'region':
            value = ''
            for region in row.region.values_list('numero',flat=True):
                value = value + str(region) + ','
            return value[:-1]
        if column == 'nombres':
            return '{0} {1}'.format(row.nombres,row.apellidos)
        if column == 'cargo':
            return row.cargo.nombre
        else:
            return super(AdministrativosRh,self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

class CargosRh(BaseDatatableView):
    """
    1.id
    2.nombre
    3.manual (retorna la url o string vacio)
    4.descripcion
    """
    model = Cargo
    columns = ['id','nombre','manual','descripcion']

    order_columns = ['','nombre','']
    max_display_length = 10

    def get_initial_queryset(self):
        return Cargo.objects.filter(oculto = False)

    def render_column(self, row, column):
        if column == 'manual':
            try:
                url = row.manual.url
            except:
                url = ""
            return url
        return super(CargosRh, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

class AdministrativosRhSoportes(BaseDatatableView):
    """
    0.id
    1.tipo
    2.fecha
    3.descripcion
    4.archivo (url o string vacio)
    5.creacion
    """
    model = Soporte
    columns = ['id','tipo','fecha','descripcion','get_archivo_url','creacion']

    order_columns = ['id','tipo','fecha','descripcion']
    max_display_length = 10

    def get_initial_queryset(self):
        return Soporte.objects.filter(oculto = False,administrativo__id=self.kwargs['id_administrativo'])

    def render_column(self, row, column):
        if column == 'tipo':
            return row.tipo.nombre
        if column == 'descripcion':
            return row.tipo.descripcion
        if column == 'get_archivo_url':
            return row.get_archivo_url()
        return super(AdministrativosRhSoportes, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(tipo__nombre__icontains=search) | Q(tipo__descripcion__icontains=search) | Q(fecha__icontains=search)
            qs = qs.filter(q)
        return qs

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