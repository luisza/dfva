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
@date: 08/10/2018
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class AuthorizationRequest(models.Model):
    #: Usuario que hace la solicitud de autorización
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #: Hora en la que se hace la solicitud
    request_date = models.DateTimeField(auto_now_add=True)
    #: Hora de la última modificación del modelo
    last_modification = models.DateTimeField(auto_now=True)
    #: El usuario ha sido autorizado ?
    authorized = models.BooleanField(default=False)
    #: El proceso de autorización ha finalizado
    finished = models.BooleanField(default=False)
    #: Quién autorizó al usuario
    who_authorized = models.ForeignKey(User, related_name="who_authorized",
                                       null=True, blank=True, on_delete=models.DO_NOTHING)
    #: Existen observaciones a la hora de autorizar a un usuario
    observations = models.TextField(null=True, blank=True)

    @property
    def terms_and_conditions(self):
        '''
        Extrae los términos y condiciones firmados por el usuario

        :return: UserConditionsAndTerms --  Modelo de términos y condiciones creado para el usuario
        '''
        return UserConditionsAndTerms.objects.get(user=self.user)

    def __str__(self):
        status = _("Denied or in check")
        if self.autorized:
            status = _("Authorized")
        return self.user.username + " ( "+status+" )"

    class Meta:
        verbose_name = _('Authorization request')
        verbose_name_plural = _('Authorizations request')


class UserConditionsAndTerms(models.Model):
    #: Usuario que firma los téminos de uso
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #: Texto para mostrar al usuario cuando firma los términos de uso
    text = models.TextField(verbose_name=_("Text"))
    #: Fecha de creación de los términos de uso, estos se crea una vez el usuario se registra usando firma digital
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Registered date"))
    #: Documento a fimar o documento firmado por el usuario
    document_signed = models.TextField(verbose_name=_("Document signed"))
    #: Determina si document_signed está firmado o no
    signed = models.BooleanField(default=False, verbose_name=_("Is signed?"))
    #: Organizacióna la que pertence el usuario
    organization = models.CharField(max_length=100, verbose_name=_("Organization"))
    #: Unidad de la organización a la que pertence el usuario
    organization_unit = models.CharField(max_length=100, verbose_name=_("Organization Unit"))
    #: Una explicación agregada por el usuario donde explica para que quiere hacer uso del sistema de firma digital
    use_reason = models.TextField(
        help_text=_("Why we have to allow you to use this digital \
        signer service?"), verbose_name=_("Use Reason"))
    #: Telefono de la persona que firma los términos de uso, permite contactarlo si algo pasa con el sistema o su aplicación
    phone = models.CharField(max_length=25, verbose_name=_("Phone"))
    #: Correo electrónico de contacto
    contact_email = models.EmailField(verbose_name=_("Contact Email"))

    def __str__(self):
        return "%s %s (signed %s)" % (self.user.username,
                                      self.organization, self.signed)
