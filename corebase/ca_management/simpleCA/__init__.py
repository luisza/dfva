import hashlib
import os
from OpenSSL import crypto
from OpenSSL.SSL import Context, TLSv1_METHOD
from django.conf import settings
from django.core.checks import Error, register
from corebase.ca_management.interface import CAManagerInterface, fix_certificate

import logging
from django.db.models.functions.base import Coalesce
logger = logging.getLogger('dfva')

@register()
def check_ca_in_settings(app_configs, **kwargs):
    errors = []
    if not (hasattr(settings, 'CA_CERT') and hasattr(settings, 'CA_KEY')):
        errors.append(Warning("CA_CERT or CA_KEY needed in settings "))
    return errors


class CAManager(CAManagerInterface):
    ca_crt = settings.CA_CERT
    ca_key = settings.CA_KEY

    def generate_certificate(self, domain, save_model):  # , ca_crt=None, ca_key=None
        """This function takes a domain name as a parameter and then creates a certificate and key with the
        domain name(replacing dots by underscores), finally signing the certificate using specified CA and 
        returns the path of key and cert files. If you are yet to generate a CA then check the top comments"""

        logger.info("SimpleCA: certificate creation request %s"%(domain,))

        # Serial Generation - Serial number must be unique for each certificate,
        # so serial is generated based on domain name
        md5_hash = hashlib.md5()
        md5_hash.update(domain.encode('utf-8'))
        serial = int(md5_hash.hexdigest(), 36)

        # The CA stuff is loaded from the same folder as this script
        ca_cert = crypto.load_certificate(
            crypto.FILETYPE_PEM, open(self.ca_crt).read())
        # The last parameter is the password for your CA key file
        ca_key = crypto.load_privatekey(
            crypto.FILETYPE_PEM, open(self.ca_key).read(), None)

        server_key = crypto.PKey()
        server_key.generate_key(crypto.TYPE_RSA, 2048)

        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()
        cert.get_subject().C = "CR"
        cert.get_subject().ST = "San Jose"
        cert.get_subject().L = "Costa Rica"
        cert.get_subject().O = save_model.name
        cert.get_subject().OU = save_model.institution_unit
        cert.get_subject().CN = domain  # This is where the domain fits
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
        cert.set_serial_number(serial)
        cert.set_issuer(ca_cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(ca_key, "sha1")
        cert.sign(ca_key, "sha256")

        save_model.private_key = crypto.dump_privatekey(
            crypto.FILETYPE_PEM, key)
        save_model.public_key = crypto.dump_publickey(
            crypto.FILETYPE_PEM, key)
        save_model.public_certificate = crypto.dump_certificate(
            crypto.FILETYPE_PEM, cert)

        save_model.server_sign_key = crypto.dump_privatekey(
            crypto.FILETYPE_PEM, server_key)
        save_model.server_public_key = crypto.dump_publickey(
            crypto.FILETYPE_PEM, server_key)
        
        logger.debug("SimpleCA: New certificate for %s is %r"%(domain, save_model.public_certificate))
        return save_model

    def check_certificate(self, certificate):
        dev = False
        try:
            dev = self._check_certificate(certificate)
        except Exception as e:
            logger.error("SimpleCA: validate EXCEPTION ", e)
            dev = False
        return dev

    def _check_certificate(self, certificate):
        new_cert = fix_certificate(certificate)

        certificate = crypto.load_certificate(
            crypto.FILETYPE_PEM, new_cert)
        serialnumber=certificate.get_serial_number()
        context = Context(TLSv1_METHOD)
        context.load_verify_locations(settings.CA_CERT)
        dev=False
        try:
            store = context.get_cert_store()

            # Create a certificate context using the store and the downloaded
            # certificate
            store_ctx = crypto.X509StoreContext(store, certificate)

            # Verify the certificate, returns None if it can validate the
            # certificate
            store_ctx.verify_certificate()

            dev=True

        except Exception as e:
            logger.error("SimpleCA: validate EXCEPTION %r"%(e,))
            dev=False
        
        logger.info("SimpleCA: validate cert %r == %r"%(serialnumber, dev ))
        return dev

    def revoke_certificate(self, certificate):
        logger.info("SimpleCA: revoke certificate, don't make anything")

