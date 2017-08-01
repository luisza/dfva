# encoding: utf-8


'''
Created on 14/4/2017

@author: luisza
'''
from __future__ import unicode_literals

import hashlib
import os

from OpenSSL import crypto


def gen_cert(domain,
             save_model,
             ca_crt,
             ca_key
             ):
    """This function takes a domain name as a parameter and then creates a certificate and key with the
    domain name(replacing dots by underscores), finally signing the certificate using specified CA and 
    returns the path of key and cert files. If you are yet to generate a CA then check the top comments"""

    # Serial Generation - Serial number must be unique for each certificate,
    # so serial is generated based on domain name
    md5_hash = hashlib.md5()
    md5_hash.update(domain.encode('utf-8'))
    serial = int(md5_hash.hexdigest(), 36)

    # The CA stuff is loaded from the same folder as this script
    ca_cert = crypto.load_certificate(
        crypto.FILETYPE_PEM, open(ca_crt).read())
    # The last parameter is the password for your CA key file
    ca_key = crypto.load_privatekey(
        crypto.FILETYPE_PEM, open(ca_key).read(), None)

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

    save_model.private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
    save_model.public_key = crypto.dump_publickey(
        crypto.FILETYPE_PEM, key)
    save_model.public_certificate = crypto.dump_certificate(
        crypto.FILETYPE_PEM, cert)

    save_model.server_sign_key = crypto.dump_privatekey(
        crypto.FILETYPE_PEM, server_key)
    save_model.server_public_key = crypto.dump_publickey(
        crypto.FILETYPE_PEM, server_key)

    return save_model
