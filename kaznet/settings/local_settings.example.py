"""
Local settings module for Kaznet
"""
from .common import INSTALLED_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'the db name',
        'USER': 'the db user',
        'PASSWORD': 'the db password',
        'HOST': '127.0.0.1'
    }
}

INSTALLED_APPS = INSTALLED_APPS + ['django_extensions', 'debug_toolbar']

CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    '127.0.0.1:9000'
)

CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

DEBUG = True
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ('127.0.0.1', '0.0.0.0')
ALLOWED_HOSTS = []