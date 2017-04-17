from cruds_adminlte.crud import ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ajax.decorators import ajax
import requests
from rest_framework.renderers import JSONRenderer

from authenticator.models import AuthenticateDataRequest
from authenticator.serializer import Authenticate_Response_Serializer
from ca.rsa import encrypt, get_hash_sum


@method_decorator(login_required, name='dispatch')
class AuthenticateDataRequestListView(ListView):
    model = AuthenticateDataRequest
    template_name = "authenticate_data_request/list.html"

    def get_queryset(self):
        queryset = super(AuthenticateDataRequestListView, self).get_queryset()
        queryset = queryset.filter(institution__user=self.request.user,
                                   institution__active=True,
                                   expiration_datetime__gte=timezone.now()
                                   )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            AuthenticateDataRequestListView, self).get_context_data(**kwargs)
        context[
            'model_verbose_name_plural'] = self.model._meta.verbose_name_plural
        return context


@method_decorator(login_required, name='dispatch')
class AuthenticateDataRequestUpdate(UpdateView):
    model = AuthenticateDataRequest
    fields = ['status', 'name']
    template_name = 'authenticate_data_request/update.html'
    success_url = reverse_lazy('authenticator_authenticatedatarequest_list')

    def get_context_data(self, **kwargs):
        context = super(
            AuthenticateDataRequestUpdate, self).get_context_data(**kwargs)
        context[
            'model_verbose_name_plural'] = self.model._meta.verbose_name_plural
        context['model_verbose_name'] = self.model._meta.verbose_name
        return context


@ajax
@login_required
def send_notification(request, token):
    adr = get_object_or_404(
        AuthenticateDataRequest, code=token, institution__user=request.user)

    ars = Authenticate_Response_Serializer(adr)
    data = JSONRenderer().render(ars.data)

    authreq = adr.authenticaterequest_set.first()
    edata = encrypt(adr.institution.public_key, data)
    hashsum = get_hash_sum(edata, authreq.algorithm)
    errors = []
    try:
        requests.post(adr.notification_url, data={'code': token,
                                                  'data': edata.decode(),
                                                  'hashsum': hashsum,
                                                  'algoritm': authreq.algorithm
                                                  })
    except Exception as e:
        errors.append(e)

    return {
        'ok': len(errors),
        'code': token,
        'errors': errors
    }
