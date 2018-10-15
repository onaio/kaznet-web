"""
Local settings module for Kaznet
"""
from celery.schedules import crontab

from .common import INSTALLED_APPS

ALLAUTH_ONA_BASE_URL = "https://api.ona.io"

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'the db name',
        'USER': 'the db user',
        'PASSWORD': 'the db password',
        'HOST': '127.0.0.1'
    }
}

# CELERY
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

CELERY_BEAT_SCHEDULE = {
    'fetch_all_instances': {
        'task': 'task_fetch_all_instances',
        'schedule': crontab(hour='*', minute='*/30'),  # every 30 min
    },
    'fetch_projects': {
        'task': 'task_fetch_projects',
        'schedule': crontab(hour='*', minute='*/15'),  # every 15 minutes
        'kwargs': {'username': 'the one username'}
    },
    'process_user_profiles': {
        'task': 'task_process_user_profiles',
        'schedule': crontab(hour='*', minute='*/30'),  # every 30 minutes
    },
    'create_filtered_data_sets': {
        'task': 'task_auto_create_filtered_data_sets',
        'schedule': crontab(hour='*', minute='*/15'),
        'kwargs': {'form_id': 'ona form id', 'project_id': 'ona project id',
                   'form_title': 'name of the form'}
    }
}

# Emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'Hello World <hello@example.com>'

INSTALLED_APPS = INSTALLED_APPS + ['django_extensions', 'debug_toolbar']

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    '127.0.0.1:3000'
)

CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST


def show_toolbar(request):
    """
    Force show toolbar
    """
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

DEBUG = True
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ('127.0.0.1', '0.0.0.0')
ALLOWED_HOSTS = []
