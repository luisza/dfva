# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 14/4/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

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
BASE_DIR = os.path.dirname(BASE_DIR)
DOC_ROOT = os.path.join(BASE_DIR, 'docs/_build/html')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!_mhp-(ve9hie2=-hcjo)svw-6mni0w0i0%^0+$5@s-1^5oj6v'

# SECURITY WARNING: don't run with debug turned on in production!
# - debug
DEBUG = True
# - enddebug
# - demo
DEMO = True  # Set False in production
ELK_LOGGING = False
# - enddemo
# - onlybccr
ONLY_BCCR = os.getenv('ONLY_BCCR', '') == 'True'
# - endonlybccr
DOCKER = False  # Is running in docker container
if os.getenv('ALLOWED_HOSTS', ''):
    ALLOWED_HOSTS = [c for c in os.getenv('ALLOWED_HOSTS', '').split(',')]
else:
    ALLOWED_HOSTS = []

MUTUAL_AUTH = os.getenv('MUTUAL_AUTH', '') == 'True'
# Application definition
DEBUG_LAST_REQUESTS=True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'corebase',
    'institution',
    'person',
    'receptor',
    'rest_framework',
    'authorization_management',
    'django_celery_beat',
    'django_celery_results',

    #'django_extensions'

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
        'DIRS': [os.path.join(BASE_DIR, 'src/templates/')],
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
# - database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# - enddatabase

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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Costa_Rica'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

CRISPY_TEMPLATE_PACK = 'bootstrap4'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_MEDIA = os.path.join(BASE_DIR, 'media/')

# Mutual Authentication (remove if not need it on development)
if MUTUAL_AUTH:
    DFVA_CA_PATH = os.path.join(BASE_DIR, 'dfva_certs/ca.crt')
    DFVA_CA_CHECK = True

# requerido para personas
DFVA_CERT_PATH = os.path.join(BASE_DIR, 'dfva_certs/dfva.crt')
DFVA_KEY_PATH = os.path.join(BASE_DIR, 'dfva_certs/dfva.key')

# tumbnails
INTERNAL_IPS = ('127.0.0.1',)

# Simple CA (remove if not used)
CA_PATH = os.path.join(BASE_DIR, 'internal_ca')
CA_CERT = os.path.join(CA_PATH, 'ca_cert.pem')
CA_KEY = os.path.join(CA_PATH, 'ca_key.pem')
# - simpleca
CA_KEY_PASSWD = None
# - endsimpleca
CA_CRL = os.path.join(CA_PATH, 'crl.pem')
CA_CERT_DURATION = 365

# - dogtag
USE_DOGTAG = os.getenv('USE_DOGTAG', '') == 'True'
# DOGTAG settings (remove if not used)
if USE_DOGTAG:
    CAMANAGER_CLASS = "corebase.ca_management.dogtag"

    DOGTAG_HOST=os.getenv('DOGTAG_HOST','ipa.mifirmadigitalcr.com')
    DOGTAG_PORT=os.getenv('DOGTAG_PORT', '8443')
    DOGTAG_SCHEME=os.getenv('DOGTAG_SCHEME','https')


    DOGTAG_AGENT_PEM_CERTIFICATE_PATH=os.path.join(
                    BASE_DIR, 'admin_cert.pem')
    DOGTAG_CERTIFICATE_SCHEME={
        'country_name': 'CR',
        'state_or_province_name': 'Costa Rica',
        'locality_name': 'San Jose',
        'organizational_unit_name': 'DFVA',
    }
    DOGTAG_CERT_REQUESTER=os.getenv('DOGTAG_CERT_REQUESTER','ucrfva')
    DOGTAG_CERT_REQUESTER_EMAIL=os.getenv('DOGTAG_CERT_REQUESTER_EMAIL','ucrfva@core.ucr.ac.cr')


if not DEBUG:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_CONTENT_TYPE_NOSNIFF=True
    SECURE_BROWSER_XSS_FILTER=True
    SESSION_COOKIE_SECURE=True
    X_FRAME_OPTIONS='DENY'
    CSRF_COOKIE_SECURE=True



# - enddogtag

ALLOWED_BCCR_IP = []  # ['192.168.1.119']

EXPIRED_DELTA = 5  # in minutes
LOGIN_REDIRECT_URL = '/'

# - fvabccr
#FVA_HOST = "http://localhost:8001/"
FVA_HOST = 'http://bccr.fva.cr/'
STUB_SCHEME = 'http'
STUB_HOST = "localhost:8001"
RECEPTOR_HOST = "http://localhost:8000/"
#RECEPTOR_HOST = 'http://bccr.fva.cr/'
#DEFAULT_NOTIFICATION_URL = r'^wcfv2\/Bccr\.Sinpe\.Fva\.EntidadDePruebas\.Notificador\/ResultadoDeSolicitud\.asmx$'
DEFAULT_NOTIFICATION_URL = r'^notifica$'
DEFAULT_BUSSINESS = 1
DEFAULT_ENTITY = 1
# - endfvabccr

RECEPTOR_CLIENT = 'receptor.client'

# Remove on production
UCR_FVA_SERVER_URL = 'http://localhost:8000'

LOGGING_ENCRYPTED_DATA = False
DFVA_REMOVE_AUTHENTICATION = 5  # minutes
DFVA_REMOVE_SIGN = 20  # minutes
DFVA_PERSON_SESSION = 25
CELERY_MODULE = "dfva.celery"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'

#from .graylog import *
from .locallog import *

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # execute 12:30 pm
    'remove_autenticacion': {
        'task': 'institution.tasks.remove_expired_authentications',
        # 'schedule': crontab(minute=30, hour=0),
        'schedule': crontab(minute='*/%d' % (DFVA_REMOVE_AUTHENTICATION, )),
    },
    'remove_sign': {
        'task': 'institution.tasks.remove_expired_signs',
        # 'schedule': crontab(minute=30, hour=0),
        'schedule': crontab(minute='*/%d' % (DFVA_REMOVE_SIGN, )),
    },
    'check_certificates': {
        'task': 'institution.tasks.notify_certs_expiration',
        # 'schedule': crontab(minute=30, hour=0),
        'schedule': crontab(day_of_week="*"),
    }
}

DEFAULT_SUCCESS_BCCR = 0
AUTHENTICATION_BACKENDS = (
    'authorization_management.authBackend.DFVABackend',
    'django.contrib.auth.backends.ModelBackend'

)

INSTITUTION_GROUP_NAME = 'Application Autors'
INSTITUION_AUTHORIZATION = 'authorization_management.terms_conditions.autorized_user_authorization'


EMAIL_PORT = 1025
EMAIL_HOST = 'localhost'

# - broker
CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
# - endbroker
