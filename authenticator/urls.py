# encoding: utf-8

'''
Free as freedom will be 14/4/2017

@author: luisza
'''

from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from authenticator.views import AuthenticateRequestViewSet

from . import views
from .institution_views import InstitutionCRUD


iviews = InstitutionCRUD()
router = routers.DefaultRouter()
router.register(r'authenticate', AuthenticateRequestViewSet)
urlpatterns = [
    url(r'^', include(iviews.get_urls())),
    url(r'^', include(router.urls)),
    # url(r'^solicita$', views.authenticate, name="authenticate"),

]
