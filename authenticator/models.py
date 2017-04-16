import uuid

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


identification_validator = RegexValidator(
    r'^(\d{9-11})$',
    message="Debe contener 9 dígitos o 11 para extranjeros y 10 cédulas jurídicas por ejemplo: 102340456 para nacionales o 10234045611 extranjeros")


# Create your models here.
class Institution(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250)
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    actived = models.BooleanField(default=True)

    domain = models.CharField(max_length=250)  # Certificate domain
    institution_unit = models.CharField(
        max_length=250, default="ND")  # UO in cert
    private_key = models.TextField()
    public_key = models.TextField()
    public_certificate = models.TextField()

    server_sign_key = models.TextField()
    server_public_key = models.TextField()


class Notification_URL(models.Model):
    description = models.CharField(max_length=250)
    url = models.URLField()
    institution = models.ForeignKey(Institution)


class Authenticate_Data_Request(models.Model):
    institution = models.ForeignKey(Institution)
    notification_url = models.URLField()
    identification = models.CharField(max_length=15,
                                      validators=[identification_validator])
    # '%Y-%m-%d %H:%M:%S',   osea  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField()
    code = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)

    STATUS = ((1, 'Solicitud recibida correctamente.'),
              (2, 'Ha ocurrido algún problema al solicitar la firma.'),
              (3, 'Solicitud con campos incompletos.'),
              (4, 'Diferencia no permitida de hora entre cliente y servidor.'),
              (5, 'La entidad no se encuentra registrada.'),
              (6, 'La entidad se encuentra en estado inactiva.'),
              (7, 'La URL no pertenece a la entidad solicitante.'),
              (8,
               'El tamaño de hash inválido debe estar entre 1 y 130 caracteres.'),
              (9, 'Algoritmo desconocido'),
              (10, 'Certificado incorrecto')
              )
    status = models.IntegerField(choices=STATUS, default=1)
    nombre = models.CharField(max_length=250, null=True)
    response_datetime = models.DateTimeField(auto_now=True)


class Authenticate_Request(models.Model):
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ALGORITHM = (
        ('sha256', 'sha256'),
        ('sha384', 'sha384'),
        ('sha512', 'sha512')
    )

    arrived_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    expirate_datetime = models.DateTimeField(null=True, blank=True)
    data_request = models.ForeignKey(
        Authenticate_Data_Request, null=True, blank=True)
    data_hash = models.CharField(
        max_length=130, help_text="""Suma hash de data tamaño máximo 130 caracteres, usando el algoritmo especificado """)
    algorithm = models.CharField(max_length=7, choices=ALGORITHM, help_text="""
    Debe ser alguno de estos : sha256, sha384, sha512
    """)
    public_certificate = models.TextField(
        help_text="""Certificado público de la institución (ver Institución) """)
    institution = models.CharField(
        max_length=50, help_text="UUID de Institutión")

    class Meta:
        ordering = ('arrived_time',)
