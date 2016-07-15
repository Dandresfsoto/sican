#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import UpdateView, TemplateView
from braces.views import LoginRequiredMixin
from usuarios.forms import UserUpdateForm
from usuarios.models import User
from sican.settings.base import MEDIA_URL
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import update_session_auth_hash
# Create your views here.
class Perfil(LoginRequiredMixin,UpdateView):
    '''
    Vista que actualiza el perfil de usuario, retorna un mensaje de confirmacion de acuerdo a la validez
    del formulario.
    '''
    template_name = "usuarios/inicio.html"
    form_class = UserUpdateForm
    success_url = "/usuario/"
    model = User

    def get_object(self):
        return User.objects.get(email=self.request.user.email)

    def form_valid(self, form):
        # take some other action here
        super(Perfil, self).form_valid(form)
        self.object = form.save()
        self.object.fullname = self.object.first_name + " " + self.object.last_name
        self.object.save()
        return self.render_to_response(self.get_context_data(form=form,mensaje='Se actualizo correctamente.'))

    def form_invalid(self, form, **kwargs):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(form=form,mensaje='No se pudo actualizar el perfil.'))

    def get_context_data(self, mensaje='',**kwargs):
        kwargs['photo_filename'] = self.object.photo_filename
        kwargs['photo_link'] = self.object.get_url_photo
        kwargs['mensaje'] = mensaje
        return super(Perfil, self).get_context_data(**kwargs)

class ChangePassword(LoginRequiredMixin,TemplateView):
    template_name = 'usuarios/changepassword.html'

    def post(self, request, *args, **kwargs):
        previus_password = request.POST['previus_password']
        new_password_1 = request.POST['new_password_1']
        new_password_2 = request.POST['new_password_2']
        user = self.request.user

        if previus_password != '' and new_password_1 != '' and new_password_2 != '':
            valid = user.check_password(previus_password)
            if valid:
                if new_password_1 != new_password_2:
                    kwargs['previus_password'] = previus_password
                    kwargs['mensaje'] = 'No se pudo cambiar la contraseña, las contraseñas no son iguales.'
                else:
                    user.set_password(new_password_1)
                    user.save()
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    update_session_auth_hash(request, user)
                    kwargs['mensaje'] = 'La contraseña se cambio correctamente.'

            else:
                kwargs['mensaje'] = "No se pudo cambiar la contraseña, debe completar todos los campos"
        else:
            kwargs['mensaje'] = "No se pudo cambiar la contraseña, debe completar todos los campos"

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)