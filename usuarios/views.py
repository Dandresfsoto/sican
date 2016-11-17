#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import UpdateView, TemplateView, FormView
from braces.views import LoginRequiredMixin
from usuarios.forms import UserUpdateForm
from usuarios.models import User
from sican.settings.base import MEDIA_URL
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import update_session_auth_hash
from usuarios.forms import ChangePasswordForm
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL
from mail_templated import send_mail

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

class ChangePassword(LoginRequiredMixin,FormView):
    form_class = ChangePasswordForm
    template_name = 'usuarios/changepassword.html'

    def get_initial(self):
        return {'user':self.request.user}

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.data['new_password_1'])
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        update_session_auth_hash(self.request, user)
        url_base = self.request.META['HTTP_ORIGIN']
        #send_mail_templated.delay('email/change_password.tpl', {'url_base':url_base,'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'password':form.data['new_password_1']}, DEFAULT_FROM_EMAIL, [user.email])
        send_mail('email/change_password.tpl', {'url_base':url_base,'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'password':form.data['new_password_1']}, DEFAULT_FROM_EMAIL, [user.email])
        return self.render_to_response(self.get_context_data(mensaje='Se cambio correctamente la contraseña'))

    def get_context_data(self, mensaje=None ,**kwargs):
        if mensaje != None:
            kwargs['mensaje'] = mensaje
        return super(ChangePassword, self).get_context_data(**kwargs)