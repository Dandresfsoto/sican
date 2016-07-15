#!/usr/bin/env python
# -*- coding: utf-8 -*-
from usuarios.models import User
from rest.serializers import UserSerializer, MensajeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from inbox.models import Mensaje
from django_datatables_view.base_datatable_view import BaseDatatableView
from administrativos.models import Administrativo
from cargos.models import Cargo
from django.db.models import Q

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
            'admin':{'name':'Administración de usuarios',
                  'icon':'icons:account-circle',
                  'id':'usuarios',
                  'links':[
                      {'name':'Listado de usuarios','link':'/admin/'},
                  ]
            },

        }


        perms_response = []
        perms_dict = {}

        for perm_user in perms_user:
            model, category = perm_user.split('.')
            if category in categories:
                perms_dict[category] = categories[category]

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
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__icontains=search)
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