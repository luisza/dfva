"""
Django settings for dfva project.

Generated by 'django-admin startproject' using Django 1.11.3

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!_mhp-(ve9hie2=-hcjo)svw-6mni0w0i0%^0+$5@s-1^5oj6v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEMO = True  # Set False in production
ALLOWED_HOSTS = []


# Application definition


INSTALLED_APPS = []
if DEMO is True:
    INSTALLED_APPS.append('demo')  # remove in production)

INSTALLED_APPS += [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corebase',
    'institution',
    'person',
    'receptor',
    'rest_framework',
    'crispy_forms',
    'django_select2',
    'easy_thumbnails',
    'image_cropping',
    'cruds_adminlte',
    'django_ajax',
    #'django_extensions',

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

ROOT_URLCONF = 'dfva.urls'

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

WSGI_APPLICATION = 'dfva.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_MEDIA = os.path.join(BASE_DIR, 'media/')


CRISPY_TEMPLATE_PACK = 'bootstrap3'
IMAGE_CROPPING_JQUERY_URL = None


INTERNAL_IPS = ('127.0.0.1',)

from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

CA_PATH = os.path.join(BASE_DIR, 'internal_ca')
CA_CERT = os.path.join(CA_PATH, 'ca_cert.pem')
CA_KEY = os.path.join(CA_PATH, 'ca_key.pem')

#CAMANAGER_CLASS="corebase.ca_management.dogtag"
DOGTAG_HOST='ipa.mifirmacr.org'
DOGTAG_PORT='8443'
DOGTAG_SCHEME='https'
DOGTAG_AGENT_PEM_CERTIFICATE_PATH=os.path.join(BASE_DIR, 'admin_cert.pem')
DOGTAG_CERTIFICATE_SCHEME={
'O': 'MIFIRMACR.ORG'    
}
DOGTAG_CERT_REQUESTER='dfva'
DOGTAG_CERT_REQUESTER_EMAIL='dfva@mifirmacr.org'

ALLOWED_BCCR_IP=[] #['192.168.1.119']

EXPIRED_DELTA = 5  # in minutes
LOGIN_REDIRECT_URL = '/'
FVA_HOST = "http://localhost:8001/"
# FVA_HOST = 'http://bccr.fva.cr/'
STUB_SCHEME = 'http'
STUB_HOST = "localhost:8001"
RECEPTOR_HOST = "http://localhost:8000/"
#RECEPTOR_HOST = 'http://bccr.fva.cr/'

DEFAULT_BUSSINESS = 1
DEFAULT_ENTITY = 1

RECEPTOR_CLIENT = 'receptor.client'

# Remove on production
UCR_FVA_SERVER_URL = 'http://localhost:8000'
DO_LOGGIN = not bool(os.environ.get('NOLOGGING', ''))

if DO_LOGGIN:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
                'formatter': 'verbose',
            },
            'file_info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/info.log'),
                'formatter': 'simple',
            },
            'remove_authentication': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/authentication.log'),
                'formatter': 'quiet',
            },
            'remove_sign': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/sign.log'),
                'formatter': 'quiet',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },

        },
        'loggers': {
            #         'dfva': {
            #             'handlers': ['file'],
            #             'level': 'DEBUG',
            #             'propagate': True,
            #         },
            'pyfva':  {
                'handlers': ['file_info'],
                'level': 'INFO',
                'propagate': True,
            },
            'dfva': {
                'handlers': ['file_info'],  # 'console',
                'level': 'INFO',
                'propagate': True,
            },
            'dfva_authentication': {
                'handlers': ['remove_authentication'],  # 'log/authentication',
                'level': 'INFO',
                'propagate': False,

            },
            'dfva_sign': {
                'handlers': ['remove_sign'],  # 'log/sign',
                'level': 'INFO',
                'propagate': False,

            }
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(asctime)s %(module)s %(message)s'
            },
            'quiet': {
                'format': '\n--- %(asctime)s ---\n %(message)s'
            },
        },
    }


DFVA_REMOVE_AUTHENTICATION = 5  # minutes
DFVA_REMOVE_SIGN = 20  # minutes
DFVA_PERSON_SESSION = 25
CELERY_MODULE = "dfva.celery"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json']

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # execute 12:30 pm
    'remove_autenticacion': {
        'task': 'institution.tasks.remove_expired_authentications',
        #'schedule': crontab(minute=30, hour=0),
        'schedule': crontab(minute='*/%d' % (DFVA_REMOVE_AUTHENTICATION, )),
    },
    'remove_sign': {
        'task': 'institution.tasks.remove_expired_signs',
        #'schedule': crontab(minute=30, hour=0),
        'schedule': crontab(minute='*/%s' % (DFVA_REMOVE_SIGN, )),
    },
}
