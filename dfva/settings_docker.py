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

from .settings import *
import os


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)
DOCKER = True
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
DOCKER = True
ALLOWED_HOSTS = [c for c in os.getenv('ALLOWED_HOSTS', '').split(',')]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', 'postgres'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'HOST': os.getenv('DATABASE_HOST', 'db'),
        'PORT': os.getenv('DATABASE_PORT', 5432)
    }
}


WSGI_APPLICATION = 'dfva.wsgi_docker.application'

STATIC_ROOT = '/dfva/static/'
STATIC_MEDIA = '/dfva/media/'

if not DEBUG:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CA_PATH = '/dfva/internal_ca/'
CA_CERT = os.path.join(CA_PATH, 'ca_cert.pem')
CA_KEY = os.path.join(CA_PATH, 'ca_key.pem')

if os.getenv('DOGTAG', 'False') == 'True':
    CAMANAGER_CLASS = "corebase.ca_management.dogtag"
DOGTAG_HOST = os.getenv('DOGTAG_HOST', 'ipa.mifirmacr.org')
DOGTAG_PORT = os.getenv('DOGTAG_PORT', '8443')
DOGTAG_SCHEME = os.getenv('DOGTAG_SCHEME', 'https')


DOGTAG_AGENT_PEM_CERTIFICATE_PATH = os.getenv(
    'DOGTAG_AGENT_PEM_CERTIFICATE_PATH', '/dfva/dogtag/admin_cert.pem')
DOGTAG_CERTIFICATE_SCHEME = {
    'O': os.getenv('DOGTAG_O', 'MIFIRMACR.ORG')
}
DOGTAG_CERT_REQUESTER = os.getenv('DOGTAG_CERT_REQUESTER', 'dfva')
DOGTAG_CERT_REQUESTER_EMAIL = os.getenv(
    'DOGTAG_CERT_REQUESTER_EMAIL', 'dfva@mifirmacr.org')

ALLOWED_BCCR_IP = [c for c in os.getenv(
    'ALLOWED_BCCR_IP', '').split(',') if c]  # [] #['192.168.1.119']

EXPIRED_DELTA = int(os.getenv('EXPIRED_DELTA', 5))  # in minutes

FVA_HOST = os.getenv('FVA_HOST', 'http://bccr.fva.cr/')
STUB_SCHEME = os.getenv('STUB_SCHEME', 'http')
STUB_HOST = os.getenv("STUB_HOST", "localhost:8001")
RECEPTOR_HOST = os.getenv('RECEPTOR_HOST', 'http://bccr.fva.cr/')

DEFAULT_BUSSINESS = os.getenv('DEFAULT_BUSSINESS', 1)
DEFAULT_ENTITY = os.getenv('DEFAULT_ENTITY', 1)


DFVA_REMOVE_AUTHENTICATION = int(
    os.getenv('DFVA_REMOVE_AUTHENTICATION', 5))  # minutes
DFVA_REMOVE_SIGN = int(os.getenv('DFVA_REMOVE_SIGN', 20))  # minutes
DFVA_PERSON_SESSION = int(os.getenv('DFVA_PERSON_SESSION', 25))
CELERY_MODULE = "dfva.celery"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json']

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
        'schedule': crontab(minute='*/%s' % (DFVA_REMOVE_SIGN, )),
    },
}
