# encoding: utf-8

'''
Free as freedom will be 14/4/2017

@author: luisza
'''

from __future__ import unicode_literals


from authenticator.views import AuthenticateRequestViewSet,\
    AuthenticatePersonRequestViewSet


def get_routes_view(router):
    router.register(r'authenticate', AuthenticateRequestViewSet)
    router.register(r'authenticate', AuthenticatePersonRequestViewSet)
