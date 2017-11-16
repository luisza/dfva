from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from corebase.models import  identification_validator,\
    BaseDocument, BaseRequestModel, ALGORITHM
from django.contrib.auth.models import User

class Person(models.Model):
    ERROR_CODE = (
        (1, 'Transacción satisfactoria'),
        (2, 'Error, persona no existe'),
        (3, 'Error no determinado')

    )
    user = models.OneToOneField(User)
    identification = models.CharField(max_length=20, primary_key=True)
    token = models.TextField(null=True, blank=True)
    cipher_token = models.TextField(null=True, blank=True)
    expiration_datetime_token = models.DateTimeField(null=True, blank=True)
    last_error_code = models.SmallIntegerField(default=1, choices=ERROR_CODE)
    authenticate_certificate = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.identification


class BasePersonRequestModel(BaseRequestModel):
    public_certificate = models.TextField(
        help_text="""Certificado público  de firma, para firma digital avanzada""")
    person = models.CharField(
        max_length=50, help_text="Identificación de la persona solicitante")

    class Meta:
        abstract = True


class PersonLogin(models.Model):
    arrived_time = models.DateTimeField(auto_now_add=True)
    public_certificate = models.TextField(
        help_text="""Certificado público  de firma, para firma digital avanzada""")
    code = models.TextField()
    person = models.CharField(
        max_length=50, help_text="Identificación de la persona solicitante")
    data_hash = models.CharField(max_length=130,
                                 help_text="""Suma hash de datos de tamaño máximo 130 caracteres, usando el
                                 algoritmo especificado """)
    algorithm = models.CharField(max_length=7, choices=ALGORITHM,
                                 help_text=""" Debe ser alguno de los siguientes: sha256, sha384, sha512""")

    def __str__(self):
        return self.person



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
        

class SignPersonDataRequest(models.Model):
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
    response_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField()
    id_transaction = models.IntegerField(default=0)
    sign_document = models.TextField(null=True, blank=True)
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
            ("view_signerdatarequest",
             "Can see available Signer Person Data Request"),
        )


class SignPersonRequest(BasePersonRequestModel):
    data_request = models.OneToOneField(
        SignPersonDataRequest,
        on_delete=models.CASCADE,
        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_signpersonrequest", "Can see available Person Sign Request"),
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

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_validatePersoncertificatedatarequest",
             "Can see available validate Person certificate Data Request"),
        )


class ValidatePersonDocumentDataRequest(BaseDocument):
    FORMATS=(
        ('cofirma', 'CoFirma'),
        ('contrafirma', 'ContraFirma'),
        ('msoffice', 'MS Office'),
        ('odf', 'Open Document Format')
        )
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
    person = models.ForeignKey(Person)
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField()
    code = models.CharField(max_length=20, default='N/D')
    format = models.CharField(max_length=15, default='n/d', choices=FORMATS)
    status = models.IntegerField(choices=STATUS, default=1)
    status_text = models.CharField(max_length=256, default='n/d')
    fue_exitosa = models.BooleanField(default=True)
    
    @property
    def id_transaction(self):
        return self.pk

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
