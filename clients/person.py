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


class PersonClientInterface():

    def register(self):
        pass

    def unregister(self):
        pass

    def authenticate(self, identification, algorithm='sha512', wait=False):
        pass

    def check_autenticate(self, identification, code, algorithm='sha512'):
        pass

    def sign(self, identification, document, algorithm='sha512', wait=False):
        pass

    def check_sign(self, identification, code):
        pass

    def validate(self, document, format='certificate'):
        pass


class PersonClient(PersonClientInterface):

    def __init__(self, person, wait_time=10, settings=Settings):
        self.person = person
        self.wait_time = wait_time
        self.settings = settings()

    def _encript(self, str_data):
        # FIXME
        return encrypt(self.settings.SERVER_PUBLIC_KEY, str_data)

    def _get_public_auth_certificate(self):
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
        edata = self._encript(str_data)
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
        edata = self._encript(str_data)
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
