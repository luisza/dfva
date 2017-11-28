'''
Created on 27 oct. 2017

@author: luis
'''

def fix_certificate(certificate):
    certificate = certificate.replace("-----BEGIN CERTIFICATE-----", '')
    certificate = certificate.replace("-----END CERTIFICATE-----", '')
    certificate = certificate.replace(" ", '\n')
    return "%s%s%s" % (
        "-----BEGIN CERTIFICATE-----",
        certificate,
        "-----END CERTIFICATE-----"
    )



class CAManagerInterface:
    def generate_certificate(self, domain, save_model):  # , ca_crt=None, ca_key=None
        pass

    def check_certificate(self, certificate):
        pass

    def revoke_certificate(self, certificate):
        pass