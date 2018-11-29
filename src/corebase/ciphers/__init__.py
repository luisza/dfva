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
@date: 14/4/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from Crypto import Random
import base64
import io

from base64 import b64decode, b64encode
import hashlib
import json

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


from Crypto.Hash import SHA512
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

BLOCK_SIZE = 16


class AES_EAX:
    @staticmethod
    def decrypt(file_in, private_key, session_key=None):
        if session_key is None:
            private_key = RSA.import_key(private_key)

            enc_session_key, nonce, tag, ciphertext = \
                [file_in.read(x)
                 for x in (private_key.size_in_bytes(), BLOCK_SIZE, 16, -1)]

            cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        return cipher_aes.decrypt_and_verify(ciphertext, tag)

    @staticmethod
    def encrypt(message, session_key, file_out):
        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(message)
        [file_out.write(x) for x in (cipher_aes.nonce, tag, ciphertext)]


class AES_256_CFB:

    @staticmethod
    def encrypt(message, session_key, file_out):
        # passphrase MUST be 16, 24 or 32 bytes long, how can I do that ?
        IV = Random.new().read(BLOCK_SIZE)
        aes = AES.new(session_key, AES.MODE_CFB, IV,  segment_size=128)
        enc_message = aes.encrypt(message)
        [file_out.write(x) for x in (IV, enc_message)]

    @staticmethod
    def decrypt(file_in, private_key, session_key=None):
        if session_key is None:
            private_key = RSA.import_key(private_key)
            enc_session_key, iv, ciphertext = \
                [file_in.read(x)
                 for x in (private_key.size_in_bytes(), BLOCK_SIZE, -1)]

            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

        aes = AES.new(session_key, AES.MODE_CFB, iv, segment_size=128)
        return aes.decrypt(ciphertext)


Available_ciphers = {
    "aes_eax": AES_EAX,
    "aes-256-cfb": AES_256_CFB
}
