import OpenSSL
from OpenSSL import crypto
from corebase.ca_management.interface import CAManagerInterface, \
    fix_certificate
from django.conf import settings
from django.core.checks import Error, register

import pki.client
import pki.profile
import pki.cert

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

    def generate_certificate(self, domain, save_model):  # , ca_crt=None, ca_key=None
        logger.info("Dogtag: certificate creation request %s" % (domain,))
        crt = crypto.X509Req()
        subject = crt.get_subject()
        for field in settings.DOGTAG_CERTIFICATE_SCHEME:
            setattr(subject, field, settings.DOGTAG_CERTIFICATE_SCHEME[field])
        subject.OU = save_model.institution_unit
        subject.CN = domain  # This is where the domain fits

        server_key = crypto.PKey()
        server_key.generate_key(crypto.TYPE_RSA, 2048)
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        crt.set_pubkey(key)
        crt.sign(key, "md5")

        inputs = {
            "cert_request_type": "pkcs10",
            "cert_request": crypto.dump_certificate_request(
                crypto.FILETYPE_PEM,
                crt).decode('utf-8'),
            "requestor_name": settings.DOGTAG_CERT_REQUESTER,
            "requestor_email": settings.DOGTAG_CERT_REQUESTER_EMAIL,
        }

        logger.debug("Dogtag: request certificate %r" % (inputs,))

        conn = self.get_connection()
        cert_client = pki.cert.CertClient(conn)
        certificates = cert_client.enroll_cert("caServerCert", inputs)
        save_model.private_key = crypto.dump_privatekey(
            crypto.FILETYPE_PEM, key)
        save_model.public_key = crypto.dump_publickey(
            crypto.FILETYPE_PEM, key)
        save_model.public_certificate = certificates[0].cert.encoded.encode()
        save_model.server_sign_key = crypto.dump_privatekey(
            crypto.FILETYPE_PEM, server_key)
        save_model.server_public_key = crypto.dump_publickey(
            crypto.FILETYPE_PEM, server_key)

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
        new_cert = fix_certificate(certificate)
        certificate = crypto.load_certificate(
            crypto.FILETYPE_PEM, new_cert)
        serialnumber = certificate.get_serial_number()

        cert_client = pki.cert.CertClient(self.get_connection())
        res = cert_client.review_cert(serialnumber)
        ca_cert_info = self.issuer_dn_to_dic(res.issuer_dn)
        user_cert_info = self.extract_dic_from_X509Name(
            certificate.get_issuer(), ca_cert_info)
        dev = res.status == 'VALID' and ca_cert_info == user_cert_info
        logger.info("Dogtag: validate cert %r == %r" % (serialnumber, dev))
        return dev

    def revoke_certificate(self, certificate):
        try:
            certificate = crypto.load_certificate(
                crypto.FILETYPE_PEM, certificate)
            cert_client = pki.cert.CertClient(self.get_connection())
            t = cert_client.revoke_cert(certificate.get_serial_number())
        except Exception as e:
            logger.error("Dogtag: revoke EXCEPTION ", e)

    def issuer_dn_to_dic(self, dn):
        dev = {}
        for keys in dn.split(','):
            key, value = keys.split("=")
            dev[key.upper()] = value.upper()
        return dev

    def extract_dic_from_X509Name(self, x509name, dn):
        dev = {}
        for key in dn.keys():
            if hasattr(x509name, key):
                dev[key] = getattr(x509name, key).upper()
        return dev
