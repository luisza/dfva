'''
Created on 12 sep. 2017

@author: luisza
'''
from institution.authenticator.views import AuthenticateRequestViewSet
from institution.signer.views import SignRequestViewSet
from institution.validator.views import ValidateInstitutionViewSet,\
    ValidateSubscriptorInstitutionViewSet
from institution.views import InstitutionCRUD
from django.conf.urls import include, url

def get_routes_view(router):
    router.register(r'authenticate', AuthenticateRequestViewSet)
    router.register(r'sign', SignRequestViewSet)
    router.register(r'validate', ValidateInstitutionViewSet)
    router.register(r'validate', ValidateSubscriptorInstitutionViewSet)
    
urlpatterns = []
try:
    # FIXME: crash when migrations are not applied
    iviews = InstitutionCRUD()

    urlpatterns = [
        url(r'^', include(iviews.get_urls())),
    ]
except:
    pass