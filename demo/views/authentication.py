'''
Created on 26 jul. 2017

@author: luis
'''

from cruds_adminlte.crud import ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ajax.decorators import ajax
from authenticator.models import AuthenticateDataRequest

from receptor.notify import send_notification as notify_send_notification


@method_decorator(login_required, name='dispatch')
class AuthenticateDataRequestListView(ListView):
    model = AuthenticateDataRequest
    template_name = "authenticate_data_request/list.html"

    def get_queryset(self):
        queryset = super(AuthenticateDataRequestListView, self).get_queryset()
        queryset = queryset.filter(institution__user=self.request.user,
                                   institution__active=True,
                                   expiration_datetime__gte=timezone.now())
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AuthenticateDataRequestListView,
                        self).get_context_data(**kwargs)
        context['model_verbose_name_plural'] = self.model._meta.verbose_name_plural
        return context


@method_decorator(login_required, name='dispatch')
class AuthenticateDataRequestUpdate(UpdateView):
    model = AuthenticateDataRequest
    fields = ['status', 'sign_document']
    template_name = 'authenticate_data_request/update.html'
    slug_field = 'code'
    slug_url_kwarg = 'token'
    success_url = reverse_lazy('authenticator_authenticatedatarequest_list')

    def get_context_data(self, **kwargs):
        context = super(AuthenticateDataRequestUpdate,
                        self).get_context_data(**kwargs)
        context['model_verbose_name_plural'] = self.model._meta.verbose_name_plural
        context['model_verbose_name'] = self.model._meta.verbose_name
        return context


@ajax
@login_required
def send_notification(request, token):
    adr = get_object_or_404(AuthenticateDataRequest,
                            code=token, institution__user=request.user)
    errors = []
    error = notify_send_notification(adr)
    if error:
        errors.append(error)
    return {'ok': len(errors), 'code': token, 'errors': errors}
