"""sican URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from sican.views import Login, Logout, Recovery, Confirmation, Proyectos
from sican.settings import base as settings
from sican.settings import dev as develop_settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^adminuser-sican/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', Login.as_view(),name='login'),
    url(r'^logout/', Logout.as_view()),
    url(r'^recovery/$', Recovery.as_view()),
    url(r'^recovery/confirmation/$', Confirmation.as_view()),
    url(r'^proyectos/', Proyectos.as_view()),
    url(r'^usuario/', include('usuarios.urls', namespace='usuarios')),
    url(r'^chat/', include('inbox.urls', namespace='inbox')),
    url(r'^rest/', include('rest.urls', namespace='rest')),
    url(r'^rh/', include('rh.urls', namespace='rh')),
    url(r'^adminuser/', include('adminuser.urls', namespace='adminuser')),
    url(r'^bases/', include('bases.urls', namespace='bases')),
    url(r'^preinscripcion/', include('preinscripcion.urls', namespace='preinscripcion')),
]

if settings.DEBUG:
    urlpatterns += static(develop_settings.MEDIA_URL, document_root=develop_settings.MEDIA_ROOT)