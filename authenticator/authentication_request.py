from cruds_adminlte.crud import ListView, UpdateView
from django.urls import reverse_lazy

from authenticator.models import AuthenticateDataRequest


class AuthenticateDataRequestListView(ListView):
    model = AuthenticateDataRequest
    template_name = "authenticate_data_request/list.html"

    def get_queryset(self):
        queryset = super(AuthenticateDataRequestListView, self).get_queryset()
        return queryset.filter(institution__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(AuthenticateDataRequestListView, self).get_context_data(**kwargs)
        context['model_verbose_name_plural'] = self.model._meta.verbose_name_plural
        return context


class AuthenticateDataRequestUpdate(UpdateView):
    model = AuthenticateDataRequest
    fields = ['status', 'name']
    template_name = 'authenticate_data_request/update.html'
    success_url = reverse_lazy('authenticator_authenticatedatarequest_list')

    def get_context_data(self, **kwargs):
        context = super(AuthenticateDataRequestUpdate, self).get_context_data(**kwargs)
        context['model_verbose_name_plural'] = self.model._meta.verbose_name_plural
        context['model_verbose_name'] = self.model._meta.verbose_name
        return context
