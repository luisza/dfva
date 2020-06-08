# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 14/4/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _

from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

import institution
from corebase.ca_management import create_certiticate, revoke_certificate
from institution.forms import InstitutionCreateForm, InstitutionEditForm, \
    NotificationUrlsForm
from institution.models import Institution, NotificationURL
from django.conf import settings

from corebase import logger


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.add_institution'),
                  name='dispatch')
class CreateInstitution(CreateView):
    """
    Permite crear una institución
    """
    model = Institution
    form_class = InstitutionCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object = create_certiticate(
                self.object.domain, self.object)
        except Exception as e:
            logger.error({'message': 'CreateInstitution: Error building certificates',
                         'data': e, 'location': __file__})
            messages.warning(
                self.request,
                _("Something was wrong building the certificates,\
                 please try again")
            )
            return self.form_invalid(form)
        self.object.user = self.request.user
        private_key = self.object.private_key
        self.object.private_key = _("\
        Private key was not stored, if you lost it, click in build new keys")
        self.object.save()
        self.object.private_key = private_key
        context = self.get_context_data()
        logger.info({'message': "CreateInstitution:", 'data':{'institution':
            self.object.name,  'username': self.request.user.username}, 'location': __file__})
        return render(self.request, 'institution/show_create_institution.html',
                      context=context)


@login_required
@permission_required('institution.change_institution')
def get_new_certificates(request, pk):
    institution = get_object_or_404(Institution, pk=pk, user=request.user)
    try:
        ok = True
        revoke_certificate(
            institution.public_certificate.decode('utf-8'))
    except Exception as e:
        ok = False
        logger.error({'message': 'Error revoking certificates', 'data':e, 'location': __file__})
        messages.warning(
            request,
            _("Something was wrong revoking certificates, please try again"))

    if ok:
        try:
            institution = create_certiticate(
                institution.domain, institution)

            private_key = institution.private_key
            institution.private_key = _("\
        Private key was not stored, if you lost it, click in build new keys")
            institution.save()
            institution.private_key = private_key
            logger.info({'message': "Regenerate keys",
                         'data': {'institution': institution.name,
                                'username': request.user.username}, 'location': __file__})
        except Exception as e:
            logger.error({'message': 'get_new_certificates: Error building certificates',
                          'data': e, 'location': __file__})
            messages.warning(
                request,
                _("Something was wrong building the certificates,\
                 please try again")
            )
    context = {'object': institution}
    return render(request, 'institution/show_create_institution.html',
                  context=context)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.change_institution'),
                  name='dispatch')
class EditInstitution(UpdateView):
    model = Institution
    form_class = InstitutionEditForm
    success_url = reverse_lazy('institution_list')

    def get_queryset(self):
        query = UpdateView.get_queryset(self)
        query = query.filter(user=self.request.user)
        return query


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.delete_institution'),
                  name='dispatch')
class DeleteInstitution(DeleteView):
    model = Institution
    success_url = reverse_lazy('institution_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        revoke_certificate(
            self.object.public_certificate.decode('utf-8'))
        logger.info({'message':"DeleteInstitution ", 'data': {'institution': self.object.name,
            'usernae': request.user.username}, 'location': __file__})
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        query = DeleteView.get_queryset(self)
        query = query.filter(user=self.request.user)
        return query


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.change_institution'),
                  name='dispatch')
class ListInstitution(ListView):
    model = Institution
    fields = ['active', 'name',  'domain']
    display_fields = ['name', 'code',  'domain',
                      'institution_unit', 'active',
                      'private_key', 'server_public_key',
                      'public_certificate']

    def get_queryset(self):
        query = ListView.get_queryset(self)
        query = query.filter(user=self.request.user).order_by('-active')
        return query


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.change_institution'),
                  name='dispatch')
class InstitutionDetail(DetailView):
    model = Institution

    def get_queryset(self):
        query = DetailView.get_queryset(self)
        query = query.filter(user=self.request.user)
        return query


@login_required
@permission_required('institution.change_institution')
def manage_notificationurls(request, pk, nu=None):
    institution = get_object_or_404(Institution, pk=pk, user=request.user)
    instance = None
    if nu is not None:
        instance = get_object_or_404(
            NotificationURL, pk=nu, institution=institution)
    if request.method == 'POST':
        form = NotificationUrlsForm(request.POST, instance=instance)
        if form.is_valid():
            noturl = form.save(commit=False)
            noturl.institution = institution
            noturl.save()
            messages.success(
                request, _('Notification Url saved succesfully'))
            form = NotificationUrlsForm(instance=None)
        else:
            messages.warning(
                request, _('Something was wrong saving the information'))
    else:
        form = NotificationUrlsForm(instance=instance)

    context = {'object': institution,
               'form': form,
               'object_list': institution.notificationurl_set.all()}
    return render(request, 'institution/notifications_urls.html',
                  context=context)


@login_required
@permission_required('institution.change_institution')
def delete_notificationurls(request, pk):
    notification_url = get_object_or_404(NotificationURL, pk=pk)
    institution = get_object_or_404(Institution,
                                    pk=notification_url.institution.pk,
                                    user=request.user)

    logger.info({'message': "Delete notification urls", 'data': {
        'institution':institution.name,
        'description': notification_url.description,
        'url': notification_url.url}, 'location': __file__})
    notification_url.delete()
    messages.success(
        request, _('Notification Url was delete succesfully'))
    return redirect(reverse_lazy("notification_urls",
                                 kwargs={'pk': institution.pk}))
