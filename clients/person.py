'''
Created on 1 ago. 2017

@author: luis
'''
import requests
from datetime import datetime
import json
from corebase.rsa import encrypt, get_hash_sum
import time
from . import Settings
from base64 import b64encode


class PersonClientInterface():

    def register(self):
        pass

    def unregister(self):
        pass

    def authenticate(self, identification, algorithm='sha512', wait=False):
        pass

    def check_autenticate(self, identification, code, algorithm='sha512'):
        pass

    def sign(self, identification, document, algorithm='sha512',
             file_path=None, _format='xml', is_base64=False,
             wait=False):
        pass

    def check_sign(self, identification, code):
        pass

    def validate(self, document, file_path=None, algorithm='sha512', _format='certificate',
                 is_base64=False):
        pass


class PersonBaseClient(PersonClientInterface):

    def __init__(self, person, wait_time=10, settings=Settings):
        self.person = person
        self.wait_time = wait_time
        self.settings = settings()

    def _encript(self, str_data, etype='authenticate'):
        """
        etype = authenticate, sign
        """
        # FIXME
        return encrypt(self.settings.SERVER_PUBLIC_KEY, str_data)

    def _get_public_auth_certificate(self):
        return self.settings.PUBLIC_CERTIFICATE

    def _get_public_sign_certificate(self):
        return self.settings.PUBLIC_CERTIFICATE

    def _get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def authenticate(self, identification, wait=False, algorithm='sha512'):
        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='authenticate')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.AUTHENTICATE_PERSON, json=params)

        data = result.json()
        if wait:
            while not data['received_notification']:
                time.sleep(self.wait_time)
                data = self.check_autenticate(
                    identification, data['code'], algorithm=algorithm)

        return data

    def check_autenticate(self, identification, code, algorithm='sha512'):
        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='authenticate')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.CHECK_AUTHENTICATE_PERSON % (code,), json=params)

        data = result.json()
        return data

    def sign(self, identification, document, resume, _format="xml",
             file_path=None, is_base64=False,
             algorithm='sha512', wait=False):
        if not is_base64:
            document = b64encode(document).decode()

        data = {
            'person': self.person,
            'document': document,
            'format': _format,
            'algorithm_hash': algorithm,
            'document_hash': get_hash_sum(document,  algorithm),
            'identification': identification,
            'resumen': resume,
            'request_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='sign')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_sign_certificate(),
            'person': self.person,
            "data": edata,
        }

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        result = requests.post(
            self.settings.FVA_SERVER_URL + self.settings.SIGN_PERSON,
            json=params, headers=headers)

        data = result.json()

        if wait:
            while not data['received_notification']:
                time.sleep(self.wait_time)
                data = self.check_sign(
                    identification, data['code'], algorithm=algorithm)

        return data

    def check_sign(self, identification, code, algorithm='sha512'):
        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='sign')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_sign_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.CHECK_SIGN_PERSON % (code,), json=params)

        data = result.json()
        return data

    def validate(self, document, file_path=None, algorithm='sha512',
                 is_base64=False,
                 _format='certificate'):

        if not is_base64:
            document = b64encode(document).decode()
        data = {
            'person': self.person,
            'document': document,
            'request_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        str_data = json.dumps(data)
        # print(str_data)
        edata = self._encript(str_data, etype='sign')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_sign_certificate(),
            'person': self.person,
            "data": edata,
        }

        if _format == 'certificate':
            url = self.settings.VALIDATE_CERTIFICATE
        else:
            url = self.settings.VALIDATE_DOCUMENT
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        result = requests.post(
            self.settings.FVA_SERVER_URL + url, json=params, headers=headers)

        return result.json()


class PersonClient(PersonBaseClient):

    def sign(self, identification, document, resume, _format="xml",
             file_path=None, is_base64=False,
             algorithm='sha512', wait=False):

        if _format not in self.settings.SUPPORTED_SIGN_FORMAT:
            raise Exception("Format not supported only %s" %
                            (",".join(self.settings.SUPPORTED_SIGN_FORMAT)))

        if file_path is None and document is None:
            raise Exception("Document or file_path must be set")

        if file_path:
            with open(file_path, 'rb') as arch:
                document = arch.read()

        if hasattr(document, 'read'):
            document = document.read()

        # if hasattr(document, 'decode'):
        #    document = document.decode()

        if resume is None:
            resume = "Sorry document with out resume"

        return super(PersonClient, self).sign(
            identification,
            document,
            resume,
            format=format,
            file_path=None,
            is_base64=is_base64,
            algorithm=algorithm,
            wait=wait)

    def validate(self, document, file_path=None, algorithm='sha512',
                 is_base64=False,
                 _format='certificate'):

        if _format not in self.settings.SUPPORTED_VALIDATE_FORMAT:
            raise Exception("Format not supported only %s" %
                            (",".join(self.settings.SUPPORTED_VALIDATE_FORMAT)))

        if file_path is None and document is None:
            raise Exception("Document or file_path must be set")

        if file_path:
            with open(file_path, 'rb') as arch:
                document = arch.read()

        if hasattr(document, 'read'):
            document = document.read()

        return super(PersonClient, self).validate(
            document,
            file_path=None,
            algorithm=algorithm,
            is_base64=is_base64,
            _format=_format)
