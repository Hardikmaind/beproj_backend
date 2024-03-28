"""
Django settings for audio_conf project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import os
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beproj-a4b03-firebase-adminsdk-xjhmt-cec8955885.json')

cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tvnorfo*zek0ndmuvm&-p(iz5@@u$8e9avp%kfl!==-_&u*qo5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

PYDUB_FFMPEG_PATH = r'C:/ffmpeg-6.1.1-essentials_build/bin/ffmpeg.exe'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'base'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'audio_conf.urls'

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

WSGI_APPLICATION = 'audio_conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# this is for the default database of django that is sqlite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# this is for the aws

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hardik',
#         'USER': 'admin',
#         'PASSWORD': 'database-1hardikdatabase-1hardik',
#         'HOST': 'database-1hardik.cp06s2y6qxxa.ap-south-1.rds.amazonaws.com',
#         'PORT': '3306',
#     }
# }

# this is for the windows xampp server
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'testing',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# this is for the  linux=>

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'be',
#         'USER': 'admin',
#         'PASSWORD': 'admin',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


# this below is for docker
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'be',
#         'USER': 'hardik',
#         'PASSWORD': 'hardik',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# this below is for railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway',
        'USER': 'root',
        'PASSWORD': 'lxIwJqnUXBPLnxRdRWcHihdjeYKaLKLf',
        'HOST': 'roundhouse.proxy.rlwy.net',
        'PORT': '47249',
    }
}






# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# REST_FRAMEWORK = {
#     # ... other settings
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # 'path.to.authentication_backends.firebase_auth',  # Replace with the correct path
#         'audio_conf.authentication_backends.FirebaseAuthentication',  # Corrected import path
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',  # Require authentication for all endpoints
#         'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Require authentication for all endpoints
#         # Add any other default permission classes here as needed
#     ],
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
