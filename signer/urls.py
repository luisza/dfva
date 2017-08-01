'''
Created on 19 jul. 2017

@author: luis
'''

from __future__ import unicode_literals
from signer.views import SignRequestViewSet, SignPersonRequestViewSet


def get_routes_view(router):
    router.register(r'sign', SignRequestViewSet)
    router.register(r'sign', SignPersonRequestViewSet)
