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
@date: 10/1/2018
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''


import traceback

import pki.cert
import pki.client
import pki.profile
import requests
from asn1crypto import pem, x509
from csrbuilder import CSRBuilder, pem_armor_csr
from django.conf import settings
from django.core.checks import register
from oscrypto import asymmetric

from corebase import logger
from corebase.ca_management.interface import CAManagerInterface


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
    log_sector = 'ca_manager'

    def __init__(self):
        self.current_host = 0
        self.client = None
        self.max_retry = len(settings.DOGTAG_HOST)

    def get_host(self):
        return settings.DOGTAG_HOST[self.current_host]

    def get_connection(self, subsystem='ca'):
        conn = pki.client.PKIConnection(settings.DOGTAG_SCHEME,
                                        self.get_host(),
                                        settings.DOGTAG_PORT, subsystem)
        conn.set_authentication_cert(
            settings.DOGTAG_AGENT_PEM_CERTIFICATE_PATH)
        return conn

    def get_client(self, req_new=False):
        if req_new:
            self.current_host = self.current_host+1 % len(settings.DOGTAG_HOST)
            self.client = None

        if self.client:
            return self.client

        conn = self.get_connection()
        self.client = pki.cert.CertClient(conn)
        return self.client

    def enroll_cert(self, inputs):
        retry = 0
        ok = False
        new_con = False
        dev = None
        while not ok and retry < self.max_retry:
            try:
                cert_client = self.get_client(req_new=new_con)
                dev = cert_client.enroll_cert("caServerCert", inputs)
                ok = True
            except requests.exceptions.ConnectionError as e:
                retry += 1
                new_con = True
                logger.error({'message': "Dogtag: Connection EXCEPTION ", 'data':e,
                              'location': __file__},
                             sector=self.log_sector)
        if retry == self.max_retry:
            raise Exception("No pki server available")
        return dev

    def generate_certificate(self, domain, save_model):
        logger.info({'message': "Dogtag: certificate creation request",
                     'data': {'domain': domain, 'model': repr(save_model)}, 'location': __file__}, sector=self.log_sector)

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

        certinputs = {
            "cert_request_type": "pkcs10",
            "cert_request": pem_armor_csr(request).decode(),
            "requestor_name": settings.DOGTAG_CERT_REQUESTER,
            "requestor_email": settings.DOGTAG_CERT_REQUESTER_EMAIL,
        }

        logger.debug({'message': "Dogtag: request certificate ", 'data':certinputs,
                      'location': __file__}, sector=self.log_sector)

        certificates = self.enroll_cert(certinputs)
        server_public_key, server_private_key = \
            asymmetric.generate_pair('rsa', bit_size=2048)

        save_model.private_key = asymmetric.dump_private_key(private_key, None)
        save_model.public_key = asymmetric.dump_public_key(public_key)
        save_model.public_certificate = certificates[0].cert.encoded.encode()

        save_model.server_sign_key = asymmetric.dump_private_key(
            server_private_key, None)
        save_model.server_public_key = asymmetric.dump_public_key(
            server_public_key)

        logger.debug({'message': "Dogtag: New certificate ", 'data':
            {'domain': domain, 'certificate': repr(save_model.public_certificate)},
                      'location': __file__}, sector=self.log_sector)
        return save_model

    def check_certificate(self, certificate):
        try:
            dev = self._check_certificate(certificate)
        except Exception as e:
            logger.error({'message':"Dogtag: validate EXCEPTION ",
                          'data': e, 'location': __file__},
                         sector=self.log_sector)
            if settings.DEBUG:
                traceback.print_exc()
            dev = False
        return dev

    def review_cert(self, serialnumber):
        retry = 0
        ok = False
        new_con = False
        dev = None
        while not ok and retry < self.max_retry:
            try:
                cert_client = self.get_client(req_new=new_con)
                dev = cert_client.review_cert(serialnumber)
                ok = True
            except requests.exceptions.ConnectionError as e:
                retry += 1
                new_con = True
                logger.error({'message':"Dogtag: Connection EXCEPTION ",
                              'data': e, 'location': __file__}, sector=self.log_sector)
        if retry == self.max_retry:
            logger.error({'message': "Dogtag: Max retry found: No pki server available",
                          'data': retry, 'location': __file__}, sector=self.log_sector)
            raise Exception("No pki server available")
        return dev

    def _check_certificate(self, certificate):
        _, _, certificate_bytes = pem.unarmor(
            certificate.encode(), multiple=False)
        certificate = x509.Certificate.load(certificate_bytes)
        serialnumber = certificate.serial_number
        res = self.review_cert(serialnumber)
        logger.debug({'message': "Dogtag: Respuesta Validando certificado: ",
                      'data': repr(res), 'location': __file__}, sector=self.log_sector)
        ca_cert_info = self.issuer_dn_to_dic(res.issuer_dn)
        user_cert_info = self.extract_dic_from_X509Name(
            certificate.issuer.native, ca_cert_info)
        dev = res.status == 'VALID' and ca_cert_info == user_cert_info
        logger.info({'message':  "Dogtag: Validando issuer  %r"%dev,
                     'data': {'ca_cert_info': repr(ca_cert_info),
                              'user_cert_info': repr(user_cert_info), 'result': repr(dev)},
                     'location': __file__}, sector=self.log_sector)
        return dev

    def revoke_request(self, serialnumber):
        retry = 0
        ok = False
        new_con = False
        dev = None
        while not ok and retry < self.max_retry:
            try:
                cert_client = self.get_client(req_new=new_con)
                dev = cert_client.revoke_cert(serialnumber)
                ok = True
            except requests.exceptions.ConnectionError as e:
                retry += 1
                new_con = True
                logger.error({'message': "Dogtag: Connection EXCEPTION ",
                              'data': e, 'location': __file__}, sector=self.log_sector)
        if retry == self.max_retry:
            raise Exception("No pki server available")
        return dev

    def revoke_certificate(self, certificate):
        try:
            _, _, certificate_bytes = pem.unarmor(
                certificate.encode(), multiple=False)
            certificate = x509.Certificate.load(certificate_bytes)

            t = self.revoke_request(certificate.serial_number)
            logger.debug({'message': "Dogtag: Respuesta revocar certificado: ",
                          'data': repr(t), 'location': __file__}, sector=self.log_sector)
        except Exception as e:
            if settings.DEBUG:
                traceback.print_exc()
            logger.error({'message':"Dogtag: revoke EXCEPTION ", 'data': e, 'location': __file__},
                         sector=self.log_sector)

    def issuer_dn_to_dic(self, dn):
        dev = {}
        for keys in dn.split(','):
            key, value = keys.split("=")
            dev[key.upper()] = value.upper()
        return dev

    def extract_dic_from_X509Name(self, x509name, dn):
        replacement = {'CN': 'common_name', 'O': 'organization_name', 'OU': 'organizational_unit_name'}

        dev = {}
        for key in dn.keys():
            if key in replacement:
                dev[key] = x509name[replacement[key]].upper()
        return dev
