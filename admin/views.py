from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from usuarios.models import User
from usuarios.forms import UserUpdateAdminForm, UserNewAdminForm, GroupNewAdminForm
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL
from django.shortcuts import HttpResponseRedirect
import random
import string
from django.contrib.auth.models import Group
# Create your views here.

class UserListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'admin/admin.html'
    permission_required = "admin.usuarios"

class UpdateUserView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = User
    form_class = UserUpdateAdminForm
    pk_url_kwarg = 'pk'
    success_url = '/admin/usuarios/'
    template_name = 'admin/editarUsuario.html'
    permission_required = "admin.usuarios"

    def get_context_data(self, **kwargs):
        kwargs['email'] = self.object.email
        return super(UpdateUserView, self).get_context_data(**kwargs)

class NewUserView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = User
    form_class = UserNewAdminForm
    success_url = '/admin/usuarios/'
    template_name = 'admin/nuevo.html'
    permission_required = "admin.usuarios"

    def form_valid(self, form):
        form.save()
        user = User.objects.get(email=form.data['email'])

        password = "".join( [random.choice(string.letters) for i in xrange(6)] )
        user.set_password(password)
        user.save()
        send_mail_templated.delay('email/new_user.tpl',
                                  {'first_name': user.first_name, 'last_name': user.last_name,
                                   'email': user.email, 'password':password},
                                  DEFAULT_FROM_EMAIL,[form.data['email']])
        return HttpResponseRedirect('/admin/usuarios/')

class GroupListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'admin/grupos.html'
    permission_required = "admin.usuarios"

class NewGroupView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Group
    form_class = GroupNewAdminForm
    success_url = '/admin/grupos/'
    template_name = 'admin/nuevoGrupo.html'
    permission_required = "admin.usuarios"

class UpdateGrupoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Group
    form_class = GroupNewAdminForm
    pk_url_kwarg = 'pk'
    success_url = '/admin/grupos/'
    template_name = 'admin/editarGrupo.html'
    permission_required = "admin.usuarios"

    def get_context_data(self, **kwargs):
        kwargs['nombre_grupo'] = self.object.name
        return super(UpdateGrupoView, self).get_context_data(**kwargs)

class DeleteGrupoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Group
    pk_url_kwarg = 'pk'
    success_url = '/admin/grupos/'
    template_name = 'admin/eliminarGrupo.html'
    permission_required = "admin.usuarios"

    def get_context_data(self, **kwargs):
        kwargs['nombre_grupo'] = self.object.name
        result = []
        permisos = Group.objects.get(id=self.object.id).permissions.all()
        for permiso in permisos:
            result.append(permiso.__str__())
        kwargs['permisos'] = result
        return super(DeleteGrupoView, self).get_context_data(**kwargs)