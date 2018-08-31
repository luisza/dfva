from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

identification_validator = RegexValidator(
    r'"(^[1|5]\d{11}$)|(^\d{2}-\d{4}-\d{4}$)"',
    message=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000"))

ALGORITHM = (
    ('sha256', 'sha256'),
    ('sha384', 'sha384'),
    ('sha512', 'sha512')
)

SUPPORTED_DOC_FORMAT = ['xml_cofirma', 'xml_contrafirma', 'odf', 'msoffice']


class BaseRequestModel(models.Model):
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    arrived_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    data_hash = models.CharField(max_length=130,
                                 help_text=_("""Suma hash de datos de tamaño máximo 130 caracteres, usando el
                                 algoritmo especificado """))
    algorithm = models.CharField(max_length=7, choices=ALGORITHM,
                                 help_text=_(""" Debe ser alguno de los siguientes: sha256, sha384, sha512"""))

    class Meta:
        abstract = True


class WarningReceived(models.Model):
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.description


class ErrorFound(models.Model):
    code = models.CharField(max_length=250)
    detail = models.TextField()

    def __str__(self):
        return self.code


class Signer(models.Model):
    identification_number = models.CharField(max_length=25)
    signature_date = models.DateField()
    full_name = models.CharField(max_length=25)

    def __str__(self):
        return self.full_name


class BaseDocument(models.Model):
    warnings = models.ManyToManyField(WarningReceived)
    errors = models.ManyToManyField(ErrorFound)
    signers = models.ManyToManyField(Signer)


class UserConditionsAndTerms(models.Model):
    user = models.ForeignKey(User)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    document_signed = models.TextField()
    signed = models.BooleanField(default=False)

    organization = models.CharField(max_length=100)
    organization_unit = models.CharField(max_length=100)
    use_reason = models.TextField(
        help_text=_("¿Porqué nosotros deberíamos permitirle usar el servicio de firma?"))
    phone = models.CharField(max_length=25)
    contact_email = models.EmailField()
