import uuid

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from corebase.models import Institution, identification_validator,\
    Person, BaseInstitutionRequestModel, BasePersonRequestModel


class ValidateCertificateDataRequest(models.Model):
    institution = models.ForeignKey(Institution)
    notification_url = models.URLField()
    identification = models.CharField(
        max_length=15, null=True, validators=[identification_validator],
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
    response_datetime = models.DateTimeField(auto_now=True)
    fue_exitosa = models.BooleanField(default=True)
    nombre_completo = models.CharField(max_length=250, null=True)
    inicio_vigencia = models.DateTimeField(null=True)
    fin_vigencia = models.DateTimeField(null=True)

    @property
    def id_transaction(self):
        return self.pk

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_validatecertificatedatarequest",
             "Can see available validate certificate Data Request"),
        )


class ValidateCertificateRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        ValidateCertificateDataRequest,
        on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_validaterequest", "Can see available validate certificate Request"),
        )


class ValidatePersonCertificateDataRequest(models.Model):
    person = models.ForeignKey(Person)
    identification = models.CharField(
        max_length=15, null=True, validators=[identification_validator],
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
    response_datetime = models.DateTimeField(auto_now=True)
    fue_exitosa = models.BooleanField(default=True)
    nombre_completo = models.CharField(max_length=250, null=True)
    inicio_vigencia = models.DateTimeField(null=True)
    fin_vigencia = models.DateTimeField(null=True)

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_validatePersoncertificatedatarequest",
             "Can see available validate Person certificate Data Request"),
        )


class ValidatePersonCertificateRequest(BasePersonRequestModel):
    data_request = models.OneToOneField(
        ValidatePersonCertificateDataRequest,
        on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_validatePersonrequest",
             "Can see available validate certificate Request"),
        )


class Advertencia(models.Model):
    descripcion = models.CharField(max_length=512)

    def __str__(self):
        return self.descripcion


class ErrorEncontrado(models.Model):
    codigo = models.CharField(max_length=250)
    detalle = models.TextField()

    def __str__(self):
        return self.codigo


class Firmante(models.Model):
    cedula = models.CharField(max_length=25)
    fecha_de_firma = models.DateField()
    nombre_completo = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre_completo


class ValidateDocumentDataRequest(models.Model):
    institution = models.ForeignKey(Institution)
    notification_url = models.URLField()
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
    advertencias = models.ManyToManyField(Advertencia)
    errores = models.ManyToManyField(ErrorEncontrado)
    firmantes = models.ManyToManyField(Firmante)
    fue_exitosa = models.BooleanField(default=True)

    @property
    def id_transaction(self):
        return self.pk

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_validatedocumentdatarequest",
             "Can see available validate document Data Request"),
        )


class ValidateDocumentRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(ValidateDocumentDataRequest,
                                        on_delete=models.CASCADE,
                                        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_validatedocumentrequest",
             "Can see validate document Sign Request"),
        )


class ValidatePersonDocumentDataRequest(models.Model):
    person = models.ForeignKey(Person)

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
    advertencias = models.ManyToManyField(Advertencia)
    errores = models.ManyToManyField(ErrorEncontrado)
    firmantes = models.ManyToManyField(Firmante)
    fue_exitosa = models.BooleanField(default=True)

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_validatepersondocumentdatarequest",
             "Can see available validate document Data Request"),
        )


class ValidatePersonDocumentRequest(BasePersonRequestModel):
    data_request = models.OneToOneField(
        ValidatePersonDocumentDataRequest,
        on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_validatepersondocumentrequest",
             "Can see validate document Sign Request"),
        )
