"""
Django settings for TextBazaar project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
# import django_heroku
import pymysql

pymysql.install_as_MySQLdb()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ky#gv2^g+9_kxe34xa0)6mlccd$ky)^y+q$t8dj(_lc!ku)w!r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.textbazaar.me','textbazaar.me','127.0.0.1','textbazaar.herokuapp.com','textbazaar-319010.uc.r.appspot.com','backend-dot-textbazaar-319010.uc.r.appspot.com','production-dot-textbazaar-319010.uc.r.appspot.com','backend.default.textbazaar-319010.uc.r.appspot.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'mathfilters',
    # 'background_task',
    # 'django_cloud_tasks',
    'google_analytics',
    'crispy_forms',
    'blog',
    'writer'
]


PROJECT_NAME = 'textbazaar-319010'
QUEUE_REGION = 'us-central1'
QUEUE_ID = 'tasks-queue'


# DJANGO_CLOUD_TASKS={
#     'project_location_name': 'projects/{PROJECT_NAME}/locations/{QUEUE_REGION}',
#     'task_handler_root_url': '/_tasks/',
# },


GOOGLE_ANALYTICS = {
    'google_analytics_id': 'UA-201161327-1',
}

X_FRAME_OPTIONS = 'SAMEORIGIN'

CRISPY_TEMPLATE_PACK = 'bootstrap4'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TextBazaar.urls'

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

WSGI_APPLICATION = 'TextBazaar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.getenv('GAE_APPLICATION',None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST':'/cloudsql/textbazaar-319010:us-central1:bazaar-instance',
            'USER':'admin',
            'NAME':'main',
            'PASSWORD':'Text4Bazaar#'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST':'127.0.0.1',
            'PORT':'3306',
            'USER':'admin',
            'NAME':'main',
            'PASSWORD':'Text4Bazaar#'
        }
    }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# import dj_database_url

# db_from_env=dj_database_url.config()
# DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# django_heroku.settings(lo11cals())

DEFAULT_FROM_EMAIL='postmaster@mail.textbazaar.me'
EMAIL_HOST = 'smtp.eu.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@mail.textbazaar.me'
EMAIL_HOST_PASSWORD = '775bd454192d7a83dfcd2210ecae6dc8-c4d287b4-7e0df0c9'
EMAIL_USE_TLS = True
BACKGROUND_TASK_ASYNC_THREADS = 300
BACKGROUND_TASK_RUN_ASYNC = False
MAX_RUN_TIME = 320
MAX_ATTEMPTS = 5
# BACKGROUND_TASK_ASYNC_THREADS = 4

