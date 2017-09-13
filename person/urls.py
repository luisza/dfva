'''
Created on 12 sep. 2017

@author: luisza
'''
from person.authenticator.views import AuthenticatePersonRequestViewSet
from person.signer.views import SignPersonRequestViewSet
from person.validator.views import ValidatePersonViewSet,\
    ValidateSubscriptorPersonViewSet
from person.views import PersonLoginView

def get_routes_view(router):
    router.register(r'authenticate', AuthenticatePersonRequestViewSet)
    router.register(r'sign', SignPersonRequestViewSet)
    router.register(r'validate', ValidatePersonViewSet)
    router.register(r'validate', ValidateSubscriptorPersonViewSet)
    router.register(r'login', PersonLoginView)
