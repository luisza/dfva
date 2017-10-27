# encoding: utf-8


'''
Created on 14/4/2017

@author: luisza
'''
from __future__ import unicode_literals

from django.conf import settings

from corebase.ca_management.simpleCA import CAManager
CA_manag_instance = CAManager()
# When dogtag module is done this has sense
if hasattr(settings, 'USE_DOCTAG'):
    pass


def create_certiticate(domain, save_model):
    return CA_manag_instance.generate_certificate(domain, save_model)


def check_certificate(certificate):
    return CA_manag_instance.check_certificate(certificate)


def revoke_certificate(certificate):
    return CA_manag_instance.revoke_certificate(certificate)
