"""
Django settings for kaznet project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3j6wf!-l4bs2bn!sz*1#)rdoz5np^0lbgfp0s8)8j5h)y#k@3s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
KAZNET_DEFAULT_CURRENCY = 'KES'

# Application definition

INSTALLED_APPS = [
    # core django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    # third party
    'rest_framework',
    'django_prices',
    'django_filters',
    'rest_framework_gis',  # Required for CountryField in Location Model
    'django_countries',  # Required for CountryField in Location Model
    'mptt',
    'phonenumber_field',
    'allauth',
    'allauth.account',
    # custom apps
    'kaznet.apps.ona',
    'kaznet.apps.main.apps.MainConfig',
    'kaznet.apps.users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kaznet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'kaznet.wsgi.application'
SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get('KAZNET_POSTGRES_HOST', 'postgres'),
        'NAME':  os.environ.get('KAZNET_POSTGRES_NAME', 'kaznet'),
        'USER': os.environ.get('KAZNET_POSTGRES_USER', 'kaznet'),
        'PASSWORD': os.environ.get('KAZNET_POSTGRES_PASSWORD', 'kaznet')
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# Allauth
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_ADAPTER = "kaznet.apps.users.adapter.AccountAdapter"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_UNIQUE_EMAIL = True
ONA_BASE_URL = 'https://stage-api.ona.io/api/v1'
ONA_USERNAME = 'kaznettest'
ONA_PASSWORD = 'Password was here'

# try and load local_settings if present
try:
    # pylint: disable=wildcard-import
    # pylint: disable=unused-wildcard-import
    from .local_settings import *  # noqa
except ImportError:
    pass
