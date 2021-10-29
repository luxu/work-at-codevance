import os
from datetime import timedelta
from pathlib import Path
from functools import partial
from decouple import Csv, config

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt',
    'providers',
    'payments',
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

ROOT_URLCONF = 'pagseguro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'pagseguro.wsgi.application'

INTERNAL_IPS = config('INTERNAL_IPS', cast=Csv(), default='127.0.0.1')

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Cloudinary
CLOUDINARY_URL = config('CLOUDINARY_URL', default=False)

if CLOUDINARY_URL:  # pragma: no cover
    INSTALLED_APPS.remove('django.contrib.staticfiles')
    INSTALLED_APPS = [
                         'cloudinary_storage',
                         'django.contrib.staticfiles',
                         'cloudinary',
                     ] + INSTALLED_APPS

    COLLECTFAST_ENABLED = False

    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'
    STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'

default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

parse_database = partial(dj_database_url.parse, conn_max_age=600)

DATABASE_TO_TEST = config("ENVIROMENT")

if 'test' in DATABASE_TO_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }
elif 'production' in DATABASE_TO_TEST:
    DATABASES = {
        'default': config('DATABASE_URL', default=default_db_url, cast=parse_database)
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),  # na doc está JWT mas pode mudar pra Bearer.
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files (Uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

COLLECTFAST_ENABLED = False

DECIMAL_SEPARATOR = ','
USE_THOUSAND_SEPARATOR = True

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = '/login'

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
EMAIL_HOST = config("EMAIL_HOST", '0.0.0.0')
EMAIL_HOST_USER = config("EMAIL_HOST_USER", '')
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", '')
EMAIL_PORT = config("EMAIL_PORT", 1025, cast=int)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", 'webmaster@localhost')

BASE_URL = config("BASE_URL", "0.0.0.0")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
