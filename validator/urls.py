# encoding: utf-8

'''
Created on 20 jul. 2017

@author: luisza
'''

from __future__ import unicode_literals
from validator.views import ValidateInstitutionViewSet, ValidatePersonViewSet


def get_routes_view(router):
    router.register(r'validate', ValidateInstitutionViewSet)
    router.register(r'validate', ValidatePersonViewSet)
