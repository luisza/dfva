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
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from corebase import utils
from pyfva import constants
from corebase import logger

identification_validator = RegexValidator(
    r'(^[1|5]\d{11}$)|(^\d{2}-\d{4}-\d{4}$)',
    message=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000"))

ALGORITHM = (
    ('sha256', 'sha256'),
    ('sha384', 'sha384'),
    ('sha512', 'sha512')
)

SUPPORTED_DOC_FORMAT = ['xml_cofirma',
                        'xml_contrafirma', 'odf', 'msoffice', 'pdf']


class BaseRequestModel(models.Model):
    """
    Representa lo mímino que debe tener una petición encriptada
    """
    #: codigo de identificacion
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    #: hora donde se crea la solicitud
    arrived_time = models.DateTimeField(auto_now_add=True)
    #: ultima actualización de la solicitud
    update_time = models.DateTimeField(auto_now=True)
    #: suma hash de la petición recibida
    data_hash = models.CharField(max_length=130,
                                 help_text=_("""Suma hash de datos de tamaño máximo 130 caracteres, usando el
                                 algoritmo especificado """))
    #: Algoritmo con el que se calculó la suma hash
    algorithm = models.CharField(max_length=7, choices=ALGORITHM,
                                 help_text=_(""" Debe ser alguno de los siguientes: sha256, sha384, sha512"""))

    class Meta:
        abstract = True


class BaseAuthenticate(models.Model):
    """
    Es la petición básica para autenticación y firma, de esta heredarán los modelos de AuthenticateRequest y SignRequest
    """
    #: hora donde se crea la solicitud
    arrived_time = models.DateTimeField(auto_now_add=True)
    #: ultima actualización de la solicitud
    update_time = models.DateTimeField(auto_now=True)
    #: Identificación de la persona que Firma/Autentica debe ser DIMEX o cédula física
    identification = models.CharField(
        max_length=15, validators=[identification_validator],
        help_text=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000")
    )
    #: El formato usado para decomprimir '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField(
        help_text=_("""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'"""))
    #: código a mostrar al usuario, es un código usado para que las personas reconozcan la transacción
    code = models.CharField(max_length=20, default='N/D')
    #: Estado de la transacción una transacción se compone de dos partes donde se modifica el status
    #: Al principio el status representa el proceso de conexión con el BCCR y la respuesta de ejecución de la transacción
    #: durante este tiempo received_notification es False , cuando se recibe la notificación de firma, se actualiza el
    #: y se coloca received_notification como True
    status = models.IntegerField(
        default=0, choices=constants.ERRORES_AL_SOLICITAR_FIRMA)
    #: Los mensajes se actualizan igual que status, y son una fuente fiable del estado de la transacción
    #: Traduce el código del status para ser leido por personas
    status_text = models.CharField(max_length=256, default='n/d')
    #: Cuando se notifica almacena el documento en base64
    sign_document = models.TextField(null=True, blank=True)
    #: Hora en la que se recibe la notificación
    response_datetime = models.DateTimeField(auto_now=True)
    #: Hora en la que la transacción se invalida
    expiration_datetime = models.DateTimeField()
    #: ID de la transacción recibida por el BCCR
    #: Si hay error de comunicación el id_transaction es 0
    id_transaction = models.IntegerField(default=0, db_index=True)
    #: Cantidad de segundos que dura la transacción usado en DFVA_HTML
    duration = models.SmallIntegerField(default=3)
    #: Se ha recibido respuesta del BCCR con el documento firmado o un error
    received_notification = models.BooleanField(default=False)
    #: Resumen del documento, permite al usuario identificar de que se trata el documento
    #: Se muestra al usuario en DFVA_HTML
    resume = models.CharField(max_length=250, null=True, blank=True)
    #: Suma Hash del documento firmado
    hash_docsigned = models.TextField(null=True, blank=True)
    #: Id con el que se calculó el hash
    #: 0 Sha256, 1 Sha384  2 Sha512
    hash_id_docsigned = models.SmallIntegerField(default=0)

    class Meta:
        abstract = True


class BaseSign(BaseAuthenticate):
    """
    Sirve de base para construir la petición de firma
    """
    #: Formato del documento a firmar  xml_cofirma, xml_contrafirma, odf, msoffice, pdf
    document_format = models.CharField(max_length=25, default='n/d')
    #: Lugar donde se firmó el documento PDF  (solo obligatorio en PDF)
    place = models.CharField(max_length=150, null=True, blank=True)
    #: Razón de firma de PDF (solo obligatorio en PDF)
    reason = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        abstract = True


class BaseValidateCertificate(models.Model):
    """
    Sirve de base para validar certificados de persona física
    """
    #: hora donde se crea la solicitud
    arrived_time = models.DateTimeField(auto_now_add=True )
    #: ultima actualización de la solicitud
    update_time = models.DateTimeField(auto_now=True)
    #: Identificación de la persona que Firma/Autentica debe ser DIMEX o cédula física
    identification = models.CharField(
        max_length=15, null=True, validators=[identification_validator],
        help_text=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000")
    )
    #: El formato usado para decomprimir  '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField(
        help_text=_("""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'"""))
    #: Código de la transacción (no se muestra al usuario)
    code = models.CharField(max_length=20, default='N/D')
    #: El status representa el proceso de conexión con el BCCR y la respuesta de ejecución de la transacción
    status = models.IntegerField(
        choices=constants.ERRORES_VALIDA_CERTIFICADO, default=0)
    #: Los mensajes se actualizan igual que status, y son una fuente fiable del estado de la transacción
    #: Traduce el código del status para ser leido por personas
    status_text = models.CharField(max_length=256, default='n/d')
    #: Hora en la que se recibió la respuesta (validación no tiene notificación)
    response_datetime = models.DateTimeField(auto_now=True)
    #: La validación del certificado fue exitosa (El certificado es válido)
    was_successfully = models.BooleanField(default=True)
    #: Nombre completo del dueño del certificado
    full_name = models.CharField(max_length=250, null=True)
    #: Inicio del proceso de validación (para métricas)
    start_validity = models.DateTimeField(null=True)
    #: Final del proceso de validación (para métricas)
    end_validity = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class WarningReceived(models.Model):
    """
    Cuando se validan certificados y documentos se puede tener advertencias que no son consideradas como
    un error pero deben tomarse en consideración en el futuro
    """
    #: Mensaje de advertencia proporcionados por el BCCR
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.description


class ErrorFound(models.Model):
    """
    Se usa para almacenar posibles errores al validar documentos
    """
    #: Código del error encontrado
    code = models.CharField(max_length=250)
    #: Texto de descripción del error
    detail = models.TextField()

    def __str__(self):
        return self.code


class Signer(models.Model):
    """
    Describe la información de las personas firmantes
    """
    #: Número de identificación de persona física o DIMEX
    identification_number = models.CharField(max_length=25)
    #: Hora de la firma del documento
    signature_date = models.DateField()
    #: Nombre completo de la persona firmante
    full_name = models.CharField(max_length=250)

    def __str__(self):
        return self.full_name


class BaseDocument(models.Model):
    """
    Sirve de base para almacenar peticiones de validación de documentos
    """
    FORMATS = (
        ('cofirma', 'CoFirma'),
        ('contrafirma', 'ContraFirma'),
        ('msoffice', 'MS Office'),
        ('odf', 'Open Document Format'),
        ('pdf', 'PDF')
    )
    #: Advertencias durante la validación
    warnings = models.ManyToManyField(WarningReceived)
    #: Errores encontrados en el documento
    errors = models.ManyToManyField(ErrorFound)
    #: Personas firmantes
    signers = models.ManyToManyField(Signer)
    #: Hora en la que se recibió la petición por parte del usuario
    request_datetime = models.DateTimeField()
    #: Código de identificación de la transacción (No se muestra al usuario)
    code = models.CharField(max_length=40, default='N/D')
    #: Formato del documento a validar
    format = models.CharField(max_length=15, default='n/d', choices=FORMATS)
    #: El status representa el proceso de conexión con el BCCR y la respuesta de ejecución de la transacción
    status = models.IntegerField(default=0)
    #: Traduce el código del status para ser leido por personas
    status_text = models.CharField(max_length=256, default='n/d')
    #: El documento es válido
    was_successfully = models.BooleanField(default=True)
    #: Hora en la que se recibe la solicitud de validación (metricas)
    arrived_time = models.DateTimeField(auto_now_add=True)
    #: Hora en la que se recibe la respuesta de la validación por parte del BCCR
    update_time = models.DateTimeField(auto_now=True)

    def get_status_display(self):
        """
        Los códigos de status pueden significar diferentes cosas según el formato
        este método determina cual es el error

        :return: string - texto del código de status
        """
        keys = {}
        if format == 'cofirma':
            keys = dict(constants.ERRORES_VALIDAR_XMLCOFIRMA)
        elif format == 'contrafirma':
            keys = dict(constants.ERRORES_VALIDAR_XMLCONTRAFIRMA)
        elif format == 'msoffice':
            keys = dict(constants.ERRORES_VALIDAR_MSOFFICE)
        elif format == 'odf':
            keys = dict(constants.ERRORES_VALIDAR_ODF)
        elif format == 'pdf':
            keys = dict(constants.ERRORES_VALIDAR_PDF)
        if self.status in keys:
            return keys[self.status]
        return _("No code reference %d") % (self.status,)

    class Meta:
        abstract = True

class BCCR_Monitor(models.Model):
    medition_time = models.DateTimeField()
    authenticate= models.BooleanField(default=False)
    signer = models.BooleanField(default=False)
    validate_certificate = models.BooleanField(default=False)
    validate_document = models.BooleanField(default=False)
    everything_ok = models.BooleanField(default=False)

    def __str__(self):
        return "%s %r"%(
            self.medition_time,
            self.everything_ok
        )

    class Meta:
        verbose_name = "Monitor de servicios del BCCR"
        verbose_name_plural = "Estado de servicios del BCCR"

class System_Request_Metric(models.Model):
    """
    Almacena métricas por transacción, sirve para determinar cuanto dura cada parte del proceso
    """
    #: Hora en la que se inicia la llamada al BCCR
    start_bccr_call = models.DateTimeField(null=True)
    #: Hora en la que se recibe la respuesta del BCCR
    end_bccr_call = models.DateTimeField(null=True)
    #: Hora en la que se inicia el guardado en la base de datos
    start_save_database = models.DateTimeField(null=True)
    #: Hora en la que se termina de guardar en la base de datos
    end_save_database = models.DateTimeField(null=True)
    #: Codigo de estado de la transacción
    transaction_status = models.IntegerField(null=True)
    #: Descripción del código de estado
    transaction_status_text = models.CharField(max_length=350, null=True)
    #: La transacción terminó con éxito osea no hubo errores de comunicación entre las partes
    transaction_success = models.BooleanField(default=False)
    #: Hora en la que se inicia la validación del certificado de la institución
    start_check_institution_certificate  = models.DateTimeField(null=True)
    #: Hora en la que se acaba la validación del certificado de la institución
    end_check_institution_certificate = models.DateTimeField(null=True)
    #: Hora en la que se inicia la desencripción de la petición
    start_decrypt = models.DateTimeField(null=True)
    #: Hora en la que se termina de desencriptar la petición
    end_decrypt = models.DateTimeField(null=True)
    #: Hora en la que se inicia a encriptar la respuesta
    start_encryption = models.DateTimeField(null=True)
    #: Hora en la que se termina de encriptar la respuesta
    end_encryption = models.DateTimeField(null=True)
    #: Hora en la que se inicia el cálculo de la suma hash
    start_hashsum = models.DateTimeField(null=True)
    #: Hora en la que se termina el cálculo de la suma hash
    end_hashsum = models.DateTimeField(null=True)
    #: Tipo de operación que describe, osea firma, autenticación, validación
    operation_type = models.CharField(max_length=30, null=True)
    #: Duración de llamada al BCCR en segundos
    bccr_call = models.FloatField(default=0)
    #: Duración de guardado en base de datos en segundos
    save_database = models.FloatField(default=0)
    #: Duración de la verificación de certificado en segundos
    check_institution_certificate = models.FloatField(default=0)
    #: Duración en segundos de la desencripción del mensaje
    decrypt_time = models.FloatField(default=0)
    #: Duración en segundos de la encripción de la respuesta
    encrypt_time = models.FloatField(default=0)
    #: Duración total de la transacción
    total_spend_time = models.FloatField(default=0)
    #: Tamaño del request
    request_size = models.FloatField(default=0)
    #: Institucion procesada
    institution = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return " %r "%{
            'check_institution_certificate': self.check_institution_certificate,
            'decrypt_time': self.decrypt_time,
            'bccr_call': self.bccr_call,
            'save_database': self.save_database,
            'encrypt_time': self.encrypt_time,
            'total_spend_time': self.total_spend_time
        }


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.bccr_call = utils.calc_bccr_call(self)
        self.save_database = utils.calc_save_database(self)
        self.check_institution_certificate =utils.calc_check_institution_certificate(self)
        self.decrypt_time = utils.calc_decrypt_time(self)
        self.encrypt_time = utils.calc_encrypt_time(self)
        self.total_spend_time = utils.calc_total_spend_time(self)
        logger.info(
            self.serialize_dictionary(), sector='metrics'
        )
        return super(System_Request_Metric, self).save(
                    force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)

    def serialize_dictionary(self):
        dev = {}
        for data in self._meta.get_fields():
            dev[data.name] = getattr(self, data.name)
        return dev

    class Meta:
        verbose_name = "Métrica del sistema"
        verbose_name_plural = "Métricas del sistema"
