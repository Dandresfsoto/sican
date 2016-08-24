from sican.settings.base import *

INSTALLED_APPS += (
    'debug_toolbar',
)


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sican_2016',

            'USER': 'root',
            'PASSWORD': '%4nd3s2015%',
            'HOST': 'localhost',
            'PORT': '3306',
        }
}