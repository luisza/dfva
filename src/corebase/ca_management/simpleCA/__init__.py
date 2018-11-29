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
@date: 12/8/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import hashlib
import os
from django.conf import settings
from django.core.checks import Error, register
from corebase.ca_management.interface import CAManagerInterface, \
    fix_certificate

from asn1crypto import pem,  x509, crl
from oscrypto import asymmetric
from certbuilder import CertificateBuilder, pem_armor_certificate
from django.utils import timezone
from datetime import timedelta
from certvalidator import CertificateValidator, ValidationContext, errors
from crlbuilder import CertificateListBuilder
import logging


logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


@register()
def check_ca_in_settings(app_configs, **kwargs):
    errors = []
    if not (hasattr(settings, 'CA_CERT') and hasattr(settings, 'CA_KEY')):
        errors.append(Warning("CA_CERT or CA_KEY needed in settings "))
    return errors


class CAManager(CAManagerInterface):
    ca_crt = settings.CA_CERT
    ca_key = settings.CA_KEY

    def generate_certificate(self, domain, save_model):
        """This function takes a domain name as a parameter and then creates
        a certificate and key with the domain name (replacing dots
        by underscores), finally signing the certificate using specified CA and
        returns the path of key and cert files. If you are yet to generate a CA
        then check the top comments"""

        logger.info("SimpleCA: certificate creation request %s" % (domain,))

        ca_private_key = asymmetric.load_private_key(
            self.ca_key,
            password=settings.CA_KEY_PASSWD)
        ca_certificate = asymmetric.load_certificate(self.ca_crt)

        end_entity_public_key, end_entity_private_key = \
            asymmetric.generate_pair('rsa', bit_size=2048)

        builder = CertificateBuilder(
            {
                'country_name': 'CR',
                'state_or_province_name': 'San Jose',
                'locality_name': 'Costa Rica',
                'organization_name': save_model.name,
                "organizational_unit_name": save_model.institution_unit,
                'common_name': domain,
            },
            end_entity_public_key
        )
        now = timezone.now()
        builder.issuer = ca_certificate
        builder.begin_date = now
        builder.end_date = now+timedelta(settings.CA_CERT_DURATION)
        builder.key_usage = set(['digital_signature'])
        end_entity_certificate = builder.build(ca_private_key)
        # settings.CA_CERT_DURATION

        server_public_key, server_private_key = \
            asymmetric.generate_pair('rsa', bit_size=2048)

        save_model.private_key = asymmetric.dump_private_key(
            end_entity_private_key, None)
        save_model.public_key = asymmetric.dump_public_key(
            end_entity_public_key)
        save_model.public_certificate = pem_armor_certificate(
            end_entity_certificate)

        save_model.server_sign_key = asymmetric.dump_private_key(
            server_private_key, None)
        save_model.server_public_key = asymmetric.dump_public_key(
            server_public_key)

        logger.debug("SimpleCA: New certificate for %s is %r" %
                     (domain, save_model.public_certificate))
        return save_model

    def check_certificate(self, certificate):
        dev = False
        try:
            certificate = fix_certificate(certificate)
            dev = self._check_certificate(certificate)
        except Exception as e:
            logger.error("SimpleCA: validate EXCEPTION %r" % (e))
            dev = False
        return dev

    def _check_certificate(self, certificate):

        _, _, certificate_bytes = pem.unarmor(
            certificate.encode(), multiple=False)
        certificate = x509.Certificate.load(certificate_bytes)

        trust_roots = []
        with open(self.ca_crt, 'rb') as f:
            for _, _, der_bytes in pem.unarmor(f.read(), multiple=True):
                trust_roots.append(der_bytes)

        crls = []
        with open(settings.CA_CRL, 'rb') as f:
            crls.append(f.read())

        context = ValidationContext(crls=crls,
                                    trust_roots=trust_roots)

        try:
            validator = CertificateValidator(
                certificate, validation_context=context)
            result = validator.validate_usage(
                set(['digital_signature'])
            )
            dev = True
        except errors.PathValidationError as e:
            logger.debug("SimpleCA: validate PathValidationError %r" % (e))
            dev = False
        except errors.PathBuildingError as e:
            logger.debug("SimpleCA: validate PathBuildingError %r" % (e))
            dev = False
        logger.info("SimpleCA: validate cert %r == %r" %
                    (certificate.serial_number, dev))
        return dev

    def revoke_certificate(self, certificate):
        # Fixme: Esta función abre y reconstruye el crl
        # El problema es que la concurrencia puede afectar la reconstrucción
        # del crl.
        # Esto podría ayudar https://github.com/ambitioninc/django-db-mutex
        # Fixme: Este método no es eficiente pues requiere reconstruir otra
        # lista y pasar los valores de la anterior cuando debería ser
        # solamente agregar el nuevo valor, pero  no logré descifrar como
        # hacerlo
        _, _, certificate_bytes = pem.unarmor(
            certificate.encode(), multiple=False)
        certificate = x509.Certificate.load(certificate_bytes)

        ca_private_key = asymmetric.load_private_key(
            self.ca_key,
            password=settings.CA_KEY_PASSWD)
        ca_certificate = asymmetric.load_certificate(self.ca_crt)

        with open(settings.CA_CRL, 'rb') as f:
            cert_list = crl.CertificateList.load(f.read())

        builder = CertificateListBuilder(
            cert_list.issuing_distribution_point_value.native[
                'distribution_point'][0],
            ca_certificate,
            1000
        )

        for revoked_cert in cert_list[
                'tbs_cert_list']['revoked_certificates']:
            revoked_cert_serial = revoked_cert['user_certificate'].native
            revoked_time = revoked_cert['revocation_date'].native
            reason = revoked_cert['crl_entry_extensions'][0][
                'extn_value'].native
            builder.add_certificate(revoked_cert_serial, revoked_time,
                                    reason)

        builder.add_certificate(certificate.serial_number,
                                timezone.now(),
                                "cessation_of_operation")

        crl_list = builder.build(ca_private_key)

        with open(settings.CA_CRL, 'wb') as f:
            f.write(crl_list.dump())

        logger.info("SimpleCA: revoke certificate, don't make anything")
