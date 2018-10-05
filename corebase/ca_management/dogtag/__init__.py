import OpenSSL
from OpenSSL import crypto
from corebase.ca_management.interface import CAManagerInterface, \
    fix_certificate
from django.conf import settings
from django.core.checks import Error, register

import pki.client
import pki.profile
import pki.cert
from asn1crypto import pem,  x509
from oscrypto import asymmetric
from csrbuilder import CSRBuilder, pem_armor_csr
import logging
logger = logging.getLogger('dfva')


@register()
def check_ca_in_settings(app_configs, **kwargs):
    errors = []
    dogtag_settings = [
        'DOGTAG_HOST',
        'DOGTAG_PORT',
        'DOGTAG_SCHEME',
        'DOGTAG_AGENT_PEM_CERTIFICATE_PATH',
        'DOGTAG_CERTIFICATE_SCHEME',
        'DOGTAG_CERT_REQUESTER',
        'DOGTAG_CERT_REQUESTER_EMAIL']
    if hasattr(settings, 'USE_DOGTAG') and settings.USE_DOGTAG:
        for dog_settings in dogtag_settings:
            if not hasattr(settings, dog_settings):
                errors.append(Warning("%s needed in settings " %
                                      (dog_settings, )))

    return errors


class CAManager(CAManagerInterface):

    def get_connection(self, subsystem='ca'):
        conn = pki.client.PKIConnection(settings.DOGTAG_SCHEME,
                                        settings.DOGTAG_HOST,
                                        settings.DOGTAG_PORT, subsystem)
        conn.set_authentication_cert(
            settings.DOGTAG_AGENT_PEM_CERTIFICATE_PATH)
        return conn

    def generate_certificate(self, domain, save_model):
        logger.info("Dogtag: certificate creation request %s" % (domain,))

        public_key, private_key = asymmetric.generate_pair(
            'rsa', bit_size=2048)
        data = {
            'common_name': domain,
            'organization_name': save_model.name,
            'organizational_unit_name': save_model.institution_unit,
            'email_address': save_model.email
        }
        data.update(settings.DOGTAG_CERTIFICATE_SCHEME)
        builder = CSRBuilder(
            data,
            public_key
        )
        #builder.subject_alt_domains = ['codexns.io', 'codexns.com']
        request = builder.build(private_key)

        inputs = {
            "cert_request_type": "pkcs10",
            "cert_request": pem_armor_csr(request).decode(),
            "requestor_name": settings.DOGTAG_CERT_REQUESTER,
            "requestor_email": settings.DOGTAG_CERT_REQUESTER_EMAIL,
        }

        logger.debug("Dogtag: request certificate %r" % (inputs,))

        conn = self.get_connection()
        cert_client = pki.cert.CertClient(conn)
        certificates = cert_client.enroll_cert("caServerCert", inputs)

        server_public_key, server_private_key = \
            asymmetric.generate_pair('rsa', bit_size=2048)

        save_model.private_key = asymmetric.dump_private_key(private_key, None)
        save_model.public_key = asymmetric.dump_public_key(public_key)
        save_model.public_certificate = certificates[0].cert.encoded.encode()

        save_model.server_sign_key = asymmetric.dump_private_key(
            server_private_key, None)
        save_model.server_public_key = asymmetric.dump_public_key(
            server_public_key)

        logger.debug("Dogtag: New certificate for %s is %r" %
                     (domain, save_model.public_certificate))
        return save_model

    def check_certificate(self, certificate):
        try:
            dev = self._check_certificate(certificate)
        except Exception as e:
            logger.error("Dogtag: validate EXCEPTION ", e)
            dev = False
        return dev

    def _check_certificate(self, certificate):

        _, _, certificate_bytes = pem.unarmor(
            certificate.encode(), multiple=False)
        certificate = x509.Certificate.load(certificate_bytes)
        serialnumber = certificate.serial_number

        cert_client = pki.cert.CertClient(self.get_connection())
        res = cert_client.review_cert(serialnumber)
        logger.debug("Dogtag: Respuesta Validano certificado: "+repr(res))
        ca_cert_info = self.issuer_dn_to_dic(res.issuer_dn)
        user_cert_info = self.extract_dic_from_X509Name(
            certificate.issuer.native, ca_cert_info)
        dev = res.status == 'VALID' and ca_cert_info == user_cert_info
        logger.info("Dogtag: validate cert %r == %r" % (serialnumber, dev))
        return dev

    def revoke_certificate(self, certificate):
        try:
            _, _, certificate_bytes = pem.unarmor(
                certificate.encode(), multiple=False)
            certificate = x509.Certificate.load(certificate_bytes)
            cert_client = pki.cert.CertClient(self.get_connection())
            t = cert_client.revoke_cert(certificate.serial_number)
            logger.debug("Dogtag: Respuesta revocar certificado: "+repr(t))
        except Exception as e:
            print(e)
            logger.error("Dogtag: revoke EXCEPTION ", e)

    def issuer_dn_to_dic(self, dn):
        dev = {}
        for keys in dn.split(','):
            key, value = keys.split("=")
            dev[key.upper()] = value.upper()
        return dev

    def extract_dic_from_X509Name(self, x509name, dn):
        replacement = {'CN': 'common_name', 'O': 'organization_name'}

        dev = {}
        for key in dn.keys():
            if key in replacement:
                dev[key] = x509name[replacement[key]].upper()
        return dev
