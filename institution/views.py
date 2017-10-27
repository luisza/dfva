from cruds_adminlte.inline_crud import InlineAjaxCRUD
from institution.models import NotificationURL, Institution
from cruds_adminlte.crud import UserCRUDView
from corebase.ca_management import create_certiticate, revoke_certificate
from django.http.response import HttpResponseRedirect
from django.shortcuts import render


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
            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object = create_certiticate(
                    self.object.domain, self.object)
                self.object.user = self.request.user
                private_key = self.object.private_key
                self.object.private_key = "La llave privada no es almacenada, si la olvidó haga click en generar nuevas llaves"
                self.object.save()
                self.object.private_key = private_key
                self.view_type = 'detail'
                self.inlines = []
                self.display_fields = create_display_fields
                context = self.get_context_data()
                return render(self.request, 'institution/show_create_institution.html',
                              context=context)

        return CreateView

    def get_update_view(self):
        self.fields = ['active', 'name',  'domain',
                       'institution_unit', 'public_certificate', 'public_key']
        return UserCRUDView.get_update_view(self)

    def get_delete_view(self):
        DView = UserCRUDView.get_delete_view(self)

        class DeleteView(DView):
            def delete(self, request, *args, **kwargs):
                self.object = self.get_object()
                success_url = self.get_success_url()
                revoke_certificate(self.object.public_certificate)
                self.object.delete()
                return HttpResponseRedirect(success_url)
        return DeleteView