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

# tasks
CELERY_ROUTES = {
    'kaznet.apps.ona.tasks.task_fetch_missing_instances': {
        'queue': 'submissions'},
    'kaznet.apps.ona.tasks.task_fetch_form_missing_instances': {
        'queue': 'submissions'},
    'kaznet.apps.ona.tasks.task_sync_updated_instances': {
        'queue': 'submissions'},
    'kaznet.apps.ona.tasks.task_sync_form_updated_instances': {
        'queue': 'submissions'},
    'kaznet.apps.ona.tasks.task_sync_deleted_instances': {
        'queue': 'submissions'},
    'kaznet.apps.ona.tasks.task_sync_form_deleted_instances': {
        'queue': 'submissions'},
    'kaznet.apps.ona.tasks.task_fetch_projects': {'queue': 'forms'},
}

CELERY_BEAT_SCHEDULE = {
    'sync_outdated_submission_reviews': {
        'task': 'task_sync_outdated_submission_reviews',
        'schedule': crontab(hour='*/6', minute='0'),  # every 6 hours
    },
    'fetch_missing_instances': {
        'task': 'task_fetch_missing_instances',
        'schedule': crontab(hour='*', minute='*/30'),  # every 30 minutes
    },
    'sync_updated_instances': {
        'task': 'task_sync_updated_instances',
        'schedule': crontab(hour='*', minute='*/30'),  # every 30 minutes
    },
    'sync_deleted_instances': {
        'task': 'task_sync_deleted_instances',
        'schedule': crontab(hour='*', minute='*/30'),  # every 30 minutes
    },
    # onadata org forms and projects
    'fetch_org_projects': {
        'task': 'task_fetch_projects',
        'schedule': crontab(hour='*', minute='*/5'),  # every 5 minutes
        'kwargs': {'username': 'kaznet'}
    },
    'sync_deleted_projects': {
        'task': 'task_sync_deleted_projects',
        'schedule': crontab(hour='*/12', minute='0'),  # every 12 hours
        'kwargs': {'usernames': ['kaznet', 'kaznettest']}
    },
    'sync_deleted_xforms': {
        'task': 'task_sync_deleted_xforms',
        'schedule': crontab(hour='*/6', minute='0'),  # every 6 hours
        'kwargs': {'username': 'kaznet'}
    },
    # onadata user forms and projects
    'fetch_user_projects': {
        'task': 'task_fetch_projects',
        'schedule': crontab(hour='*', minute='*/5'),  # every 5 minutes
        'kwargs': {'username': 'kaznettest'}
    },
    'sync_deleted_user_xforms': {
        'task': 'task_sync_deleted_xforms',
        'schedule': crontab(hour='*/6', minute='30'),  # every 6 hours
        'kwargs': {'username': 'kaznettest'}
    },
    'task_past_end_date': {
        'task': 'task_past_end_date',
        'schedule': crontab(hour='1', minute='0'),  # once a day
    },
    'task_has_no_more_occurences': {
        'task': 'task_has_no_more_occurences',
        'schedule': crontab(hour='1', minute='30'),  # once a day
    },
    'task_ensure_bounty_exists': {
        'task': 'task_ensure_bounty_exists',
        'schedule': crontab(hour='*/6', minute='30'),  # every 6 hours
    },
    'task_sync_xform_can_submit_checks': {
        'task': 'task_sync_xform_can_submit_checks',
        'schedule': crontab(hour='*/6'),  # every 6 hours
    },
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
