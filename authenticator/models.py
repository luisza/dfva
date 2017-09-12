import uuid

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from corebase.models import Institution, identification_validator, ALGORITHM,\
    Person, BasePersonRequestModel, BaseInstitutionRequestModel


class AuthenticateDataRequest(models.Model):
    institution = models.ForeignKey(Institution)
    notification_url = models.URLField()
    identification = models.CharField(
        max_length=15, validators=[identification_validator],
        help_text="""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'""")
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField()
    code = models.CharField(max_length=20, default='N/D')

    STATUS = ((1, 'Solicitud recibida correctamente'),
              (2, 'Ha ocurrido algún problema al solicitar la firma'),
              (3, 'Solicitud con campos incompletos'),
              (4, 'Diferencia de hora no permitida entre cliente y servidor'),
              (5, 'La entidad no se encuentra registrada'),
              (6, 'La entidad se encuentra en estado inactiva'),
              (7, 'La URL no pertenece a la entidad solicitante'),
              (8, 'El tamaño de hash debe ser entre 1 y 130 caracteres'),
              (9, 'Algoritmo desconocido'),
              (10, 'Certificado incorrecto'))
    status = models.IntegerField(choices=STATUS, default=1)
    status_text = models.CharField(max_length=256, default='n/d')
    sign_document = models.TextField(null=True, blank=True)
    response_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField()
    id_transaction = models.IntegerField(default=0)
    duration = models.SmallIntegerField(default=3)
    received_notification = models.BooleanField(default=False)

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_authenticatedatarequest",
             "Can see available Authenticate Data Request"),
        )


class AuthenticateRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        AuthenticateDataRequest,
        on_delete=models.CASCADE,
        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_authenticaterequest", "Can see available Authenticate Request"),
        )


class AuthenticatePersonDataRequest(models.Model):
    person = models.ForeignKey(Person)
    identification = models.CharField(
        max_length=15, validators=[identification_validator],
        help_text="""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'""")
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField()
    code = models.CharField(max_length=20, default='N/D')

    STATUS = ((1, 'Solicitud recibida correctamente'),
              (2, 'Ha ocurrido algún problema al solicitar la firma'),
              (3, 'Solicitud con campos incompletos'),
              (4, 'Diferencia de hora no permitida entre cliente y servidor'),
              (5, 'La entidad no se encuentra registrada'),
              (6, 'La entidad se encuentra en estado inactiva'),
              (7, 'La URL no pertenece a la entidad solicitante'),
              (8, 'El tamaño de hash debe ser entre 1 y 130 caracteres'),
              (9, 'Algoritmo desconocido'),
              (10, 'Certificado incorrecto'))
    status = models.IntegerField(choices=STATUS, default=1)
    status_text = models.CharField(max_length=256, default='n/d')
    sign_document = models.TextField(null=True, blank=True)
    response_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField()
    id_transaction = models.IntegerField(default=0)
    duration = models.SmallIntegerField(default=3)
    received_notification = models.BooleanField(default=False)

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_authenticatepersondatarequest",
             "Can see available Authenticate Person Data Request"),
        )


class AuthenticatePersonRequest(BasePersonRequestModel):
    data_request = models.OneToOneField(AuthenticatePersonDataRequest,
                                        on_delete=models.CASCADE,
                                        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_authenticatepersonrequest",
             "Can see available Authenticate Person Request"),
        )
