from django.db import models
from django.core.validators import RegexValidator
import uuid

identification_validator = RegexValidator(
    r'"(^[1|5]\d{11}$)|(^\d{2}-\d{4}-\d{4}$)"',
    message="Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000")

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
                                 help_text="""Suma hash de datos de tamaño máximo 130 caracteres, usando el
                                 algoritmo especificado """)
    algorithm = models.CharField(max_length=7, choices=ALGORITHM,
                                 help_text=""" Debe ser alguno de los siguientes: sha256, sha384, sha512""")

    class Meta:
        abstract = True

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


class BaseDocument(models.Model):
    advertencias = models.ManyToManyField(Advertencia)
    errores = models.ManyToManyField(ErrorEncontrado)
    firmantes = models.ManyToManyField(Firmante)
