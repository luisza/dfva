# encoding: utf-8


'''
Created on 14/4/2017

@author: luisza
'''
from __future__ import unicode_literals

import os

from cruds_adminlte.crud import UserCRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from django.conf import settings
from django.http.response import HttpResponseRedirect

from ca.ca_management import gen_cert

from .models import Institution, NotificationURL


class NotificationURLAjaxCRUD(InlineAjaxCRUD):
    model = NotificationURL
    base_model = Institution
    inline_field = 'institution'
    fields = ['description', 'url']
    title = "Direcciones de notificación"


class InstitutionCRUD(UserCRUDView):
    model = Institution
    check_login = True
    check_perms = True
    fields = ['name', 'domain', 'institution_unit', 'active']
    list_fields = ['name', 'domain', 'institution_unit', 'active']
    display_fields = ['name', 'code',  'domain', 'institution_unit', 'active', 'private_key', 'server_public_key',
                      'public_certificate']

    inlines = [NotificationURLAjaxCRUD]

    def get_create_view(self):
        CView = UserCRUDView.get_create_view(self)

        class CreateView(CView):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object = gen_cert(self.object.domain, self.object,
                                       os.path.join(
                                           settings.CA_PATH, "ca_cert.pem"),
                                       os.path.join(settings.CA_PATH, "ca_key.pem"))
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())

        return CreateView
