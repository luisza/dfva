from django.views.generic.edit import CreateView, UpdateView, DeleteView
from institution.models import Institution, NotificationURL
from corebase.ca_management import create_certiticate, revoke_certificate
from django.contrib import messages
import logging
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.views.generic.list import ListView
from institution.forms import InstitutionEditForm, InstitutionCreateForm,\
    NotificationUrlsForm
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required
logger = logging.getLogger('dfva')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.add_institution'), name='dispatch')
class CreateInstitution(CreateView):
    model = Institution
    form_class = InstitutionCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object = create_certiticate(
                self.object.domain, self.object)
        except Exception as e:
            logger.debug(
                'Ha ocurrido un problema generando los certificados, por favor vuelva a intentarlo %r' % (e,))
            messages.warning(
                self.request, 'Ha ocurrido un problema generando los certificados, por favor vuelva a intentarlo')
            return self.form_invalid(form)
        self.object.user = self.request.user
        private_key = self.object.private_key
        self.object.private_key = "La llave privada no es almacenada, si la olvidó haga click en generar nuevas llaves"
        self.object.save()
        self.object.private_key = private_key
        context = self.get_context_data()
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
        logger.debug(
            'Ha ocurrido un problema revocando los certificados, por favor vuelva a intentarlo %r' % (e,))
        messages.warning(
            request, 'Ha ocurrido un problema revocando los certificados, por favor vuelva a intentarlo')

    if ok:
        try:
            institution = create_certiticate(
                institution.domain, institution)

            private_key = institution.private_key
            institution.private_key = "La llave privada no es almacenada, si la olvidó haga click en generar nuevas llaves"
            institution.save()
            institution.private_key = private_key
        except Exception as e:
            logger.debug(
                'Ha ocurrido un problema generando los certificados, por favor vuelva a intentarlo %r' % (e,))
            messages.warning(
                request, 'Ha ocurrido un problema generando los certificados, por favor vuelva a intentarlo')

    context = {'object': institution}
    return render(request, 'institution/show_create_institution.html',
                  context=context)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.change_institution'), name='dispatch')
class EditInstitution(UpdateView):
    model = Institution
    form_class = InstitutionEditForm
    success_url = reverse_lazy('institution_list')

    def get_queryset(self):
        query = UpdateView.get_queryset(self)
        query = query.filter(user=self.request.user)
        return query


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.delete_institution'), name='dispatch')
class DeleteInstitution(DeleteView):
    model = Institution
    success_url = reverse_lazy('institution_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        revoke_certificate(
            self.object.public_certificate.decode('utf-8'))
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        query = DeleteView.get_queryset(self)
        query = query.filter(user=self.request.user)
        return query


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('institution.change_institution'), name='dispatch')
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
@method_decorator(permission_required('institution.change_institution'), name='dispatch')
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
                request, 'Url guardada satisfactoriamente')
            form = NotificationUrlsForm(instance=None)
        else:
            messages.warning(
                request, 'Ha sucedido un error guardando la información')
    else:
        form = NotificationUrlsForm(instance=instance)

    context = {'object': institution,
               'form': form,
               'object_list': institution.notificationurl_set.all()}
    return render(request, 'institution/notifications_urls.html',
                  context=context)
