from cruds_adminlte.inline_crud import InlineAjaxCRUD
from institution.models import NotificationURL, Institution
from cruds_adminlte.crud import UserCRUDView
from corebase.ca_management import create_certiticate
from django.http.response import HttpResponseRedirect


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
                self.object = create_certiticate(
                    self.object.domain, self.object)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())

        return CreateView
