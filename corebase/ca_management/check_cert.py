# encoding: utf-8


'''
Created on 16/4/2017

@author: luisza
'''
from __future__ import unicode_literals

import os

from OpenSSL import crypto
from OpenSSL.SSL import Context, TLSv1_METHOD
from django.conf import settings


#os.path.join(settings.CA_PATH, "ca_cert.pem")
def fix_certificate(certificate):
    certificate = certificate.replace("-----BEGIN CERTIFICATE-----", '')
    certificate = certificate.replace("-----END CERTIFICATE-----", '')
    certificate = certificate.replace(" ", '\n')
    return "%s%s%s" % (
        "-----BEGIN CERTIFICATE-----",
        certificate,
        "-----END CERTIFICATE-----"
    )


def _check_certificate(certificate):
    new_cert = fix_certificate(certificate)

    certificate = crypto.load_certificate(
        crypto.FILETYPE_PEM, new_cert)

    context = Context(TLSv1_METHOD)
    context.load_verify_locations(
        os.path.join(settings.CA_PATH, "ca_cert.pem"))

    try:
        store = context.get_cert_store()

        # Create a certificate context using the store and the downloaded
        # certificate
        store_ctx = crypto.X509StoreContext(store, certificate)

        # Verify the certificate, returns None if it can validate the
        # certificate
        store_ctx.verify_certificate()

        return True

    except Exception as e:
        return False


def check_certificate(certificate):
    dev = False
    try:
        dev = _check_certificate(certificate)
    except:
        pass
    return dev
