# encoding: utf-8


'''
Created on 16/4/2017

@author: luisza
'''
from __future__ import unicode_literals

from base64 import b64decode, b64encode
import hashlib
import json

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def get_digest(digest_name):
    if 'sha256':
        return hashlib.sha256()
    elif 'sha384':
        return hashlib.sha384()
    elif 'sha512':
        return hashlib.sha512()


def get_hash_sum(data, algorithm):
    if type(data) == str:
        data = data.encode()
    digest = get_digest(algorithm)
    digest.update(data)
    hashsum = digest.hexdigest()
    return hashsum


def decrypt(private_key, cipher_text):
    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    raw_cipher_data = b64decode(cipher_text)
    decrypted = rsakey.decrypt(raw_cipher_data)
    return json.loads(decrypted.decode())


def encrypt(public_key, message):
    if type(message) == str:
        message = message.encode('utf-8')
    rsakey = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(rsakey)
    ciphertext = cipher.encrypt(message)
    return b64encode(ciphertext)
