#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from usuarios.extra import ContentTypeRestrictedFileField
import os
from sican.settings.base import STATIC_URL
from cargos.models import Cargo


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        try:
            user = self.get(email=email)
        except:
            user = self.create(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    objects = UserManager()
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    cargo = models.ForeignKey(Cargo,default=1)
    telefono_corporativo = models.CharField(max_length=10,blank=True)
    telefono_personal = models.CharField(max_length=10,blank=True)
    correo_personal = models.EmailField(max_length=100,blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    recovery = models.CharField(max_length=20,null=True,blank=True,default="")
    new_password = models.CharField(max_length=100,null=True,blank=True,default="")
    photo = ContentTypeRestrictedFileField(upload_to='Usuarios/Foto',blank=True,null=True,content_types=['image/jpg', 'image/jpeg', 'image/png'],max_upload_size=1048576)


    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email

    def photo_filename(self):
        return os.path.basename(self.photo.name)

    def get_photo(self):
        photo = self.photo
        if photo.name == '':
            avatar = STATIC_URL+"img/unknown-user.png"
        else:
            avatar = photo.url
        return avatar

    def get_url_photo(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url

    def photo_filename(self):
        return os.path.basename(self.photo.name)