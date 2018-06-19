'''
Created on 18 jun. 2018

@author: luis
'''
from django.contrib import messages
from django.utils.translation import gettext as _


def authorize_user(request, user):
    messages.success(request,
                     _("Congrats!, Your can now add applications"))
    return True
