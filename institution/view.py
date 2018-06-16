"""
from institution.cruds.inline_crud import InlineAjaxCRUD
from institution.models import NotificationURL, Institution
from institution.cruds.crud import UserCRUDView
from corebase.ca_management import create_certiticate, revoke_certificate
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

import logging
logger = logging.getLogger('dfva')


class NotificationURLAjaxCRUD(InlineAjaxCRUD):
    model = NotificationURL
    base_model = Institution
    inline_field = 'institution'
    fields = ['description', 'url', 'not_webapp']
    title = "Direcciones de notificación"


class InstitutionCRUD(UserCRUDView):
    model = Institution
    check_login = True
    check_perms = True
    fields = ['active', 'name',  'domain', 'institution_unit']
    list_fields = ['name', 'domain', 'institution_unit', 'active']
    display_fields = ['name', 'code',  'domain', 'institution_unit', 'active', 'private_key', 'server_public_key',
                      'public_certificate']

    inlines = [NotificationURLAjaxCRUD]

    def get_create_view(self):
        self.fields = ['active', 'name',  'domain', 'institution_unit']
        CView = UserCRUDView.get_create_view(self)
        create_display_fields = self.display_fields

        class CreateView(CView):
            

        return CreateView

    def get_update_view(self):
        self.fields = ['active', 'name',  'domain',
                       'institution_unit', 'public_certificate', 'public_key']
        return UserCRUDView.get_update_view(self)

    def get_delete_view(self):
        DView = UserCRUDView.get_delete_view(self)

        class DeleteView(DView):

        return DeleteView
"""