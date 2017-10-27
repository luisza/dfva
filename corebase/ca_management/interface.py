'''
Created on 27 oct. 2017

@author: luis
'''


class CAManagerInterface:
    def generate_certificate(self, domain, save_model):  # , ca_crt=None, ca_key=None
        pass

    def check_certificate(self, certificate):
        pass

    def revoke_certificate(self, certificate):
        pass