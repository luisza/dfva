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
@date: 12/9/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import importlib
from django.conf import settings
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from institution.models import AuthenticateDataRequest, SignDataRequest,\
    Institution
from institution.authenticator.serializer import \
    LogAuthenticateInstitutionRequestSerializer
from institution.signer.serializer import LogSingInstitutionRequestSerializer
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string

app = importlib.import_module(settings.CELERY_MODULE).app
import logging
logger_auth = logging.getLogger('dfva_authentication')
logger_sign = logging.getLogger('dfva_sign')


@app.task
def remove_expired_authentications():

    basetime = timezone.now() - timezone.timedelta(minutes=settings.DFVA_REMOVE_AUTHENTICATION)
    queryset = AuthenticateDataRequest.objects.filter(
        expiration_datetime__lte=basetime
    )
    if queryset.exists():
        data = LogAuthenticateInstitutionRequestSerializer(queryset, many=True)
        json = JSONRenderer().render(data.data).decode('utf-8')
        logger_auth.info(json)
        queryset.delete()


@app.task
def remove_expired_signs():
    basetime = timezone.now() - timezone.timedelta(minutes=settings.DFVA_REMOVE_SIGN)
    queryset = SignDataRequest.objects.filter(
        expiration_datetime__lte=basetime
    )

    if queryset.exists():
        data = LogSingInstitutionRequestSerializer(queryset, many=True)
        json = JSONRenderer().render(data.data).decode('utf-8')
        logger_sign.info(json)
        queryset.delete()


def get_url():
    url = 'localhost:8000'
    http = 'http'
    if settings.ALLOWED_HOSTS:
        url = settings.ALLOWED_HOSTS.pop()
        http = "https"
        if url == '*':
            url = "localhost:8000"
            http = "http"

    return http + "://" + url


def is_today(date1, date2):
    dev = all((
        date1.day == date2.day,
        date1.month == date2.month,
        date1.year == date2.year
    ))
    return dev


def notify_certificate_expiration(now):
    for institution in Institution.objects.all():
        certdate = institution.get_expiration_date()
        week1 = relativedelta(weeks=1)
        week2 = relativedelta(weeks=2)
        week3 = relativedelta(weeks=4)
        d1 = relativedelta(days=1)
        d2 = relativedelta(days=2)
        ok = any((
            is_today(certdate, now + week1),
            is_today(certdate, now + week2),
            is_today(certdate, now + week3),
            is_today(certdate, now + d1),
            is_today(certdate, now + d2)
        ))

        if ok:
            send_mail(
                'Importante certificado a punto de vencer',
                'Revice sus certificados en DFVA.',
                settings.DEFAULT_FROM_EMAIL,
                [institution.email],

                html_message=render_to_string(
                    'institution/email/institution_certificate_mail.html',
                    {'object': institution,
                     'domain': get_url()}
                ),
                fail_silently=False
            )


@app.task
def notify_certs_expiration():
    now = timezone.now()
    notify_certificate_expiration(now)
