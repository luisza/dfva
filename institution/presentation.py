# encoding: utf-8


'''
Created on 17/4/2017

@author: luisza
'''
from __future__ import unicode_literals
from django.utils.safestring import mark_safe


class PEMpresentation(object):

    def present(self, data):
        return mark_safe("<pre>%s</pre>" % (data))

    def get_private_key_display(self):
        return self.present(self.private_key)

    def get_public_key_display(self):
        return self.present(self.public_key)

    def get_public_certificate_display(self):
        return self.present(self.public_certificate)

    def get_server_sign_key_display(self):
        return self.present(self.server_sign_key)

    def get_server_public_key_display(self):
        return self.present(self.server_public_key)
