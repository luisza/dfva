'''
Created on 2 ago. 2017

@author: luis
'''

# Requiere pyasn1 pyasn1_modules  python-pkcs11
import pkcs11
import os
from pkcs11.constants import Attribute
from pkcs11.constants import ObjectClass
import OpenSSL


def NO_USAR_ESTO_ES_PARA_TESTING():
    # Initialise our PKCS#11 library
    lib = pkcs11.lib(os.environ['PKCS11_MODULE'])
    # FIXME: Multiples slots
    slot = lib.get_slots()[0]
    token = slot.get_token()
    session = token.open(user_pin=os.environ['PKCS11_PIN'])
    certs = {}
    cert_label = []
    for cert in session.get_objects({
            Attribute.CLASS: ObjectClass.CERTIFICATE}):
        x509 = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_ASN1, cert[Attribute.VALUE])
        certs[cert[3]] = {
            'cert': cert,
            'pub_key': OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, x509.get_pubkey()),
            'pem': OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, x509),
        }
        cert_label.append(cert[3])

    for privkey in session.get_objects({Attribute.CLASS: ObjectClass.PRIVATE_KEY}):
        if privkey.label in certs:
            certs[privkey.label]['priv_key'] = privkey

    # Verificando

    from Crypto.Hash import SHA512
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.PublicKey import RSA

    message = b"Hello world"
    digest = SHA512.new()
    digest.update(message)
    # i = client.certificates['authentication']['priv_key']
    # cert=client.certificates['authentication']['pem']
    #sig = i.sign(message)

    #pub_key = RSA.importKey(cert)
    #verifier = PKCS1_v1_5.new(pub_key)
    #verifier.verify(digest, sig)

    from base64 import b64decode
    from Crypto.Cipher import AES, PKCS1_OAEP
    import io
    data = b'poner datos cifrados aqui'
    raw_cipher_data = b64decode(data)
    file_in = io.BytesIO(raw_cipher_data)
    file_in.seek(0)
    enc_session_key, nonce, tag, ciphertext = [
        file_in.read(x) for x in (256, 16, 16, -1)]
    cipher_aes = AES.new(token, AES.MODE_EAX, nonce)
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)
