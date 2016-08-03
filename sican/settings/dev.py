from sican.settings.base import *

INSTALLED_APPS += (
    'debug_toolbar',
)


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sican',

            'USER': 'sican',
            'PASSWORD': 'sican12345%',
            'HOST': 'localhost',
            'PORT': '3306',
        }
}