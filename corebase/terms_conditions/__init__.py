from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from corebase.forms import UserConditionsAndTermsForm
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from corebase.models import UserConditionsAndTerms
from pyfva.clientes.firmador import ClienteFirmador
from django.conf import settings
from base64 import b64encode
from corebase.rsa import get_hash_sum
import logging
from institution.models import SignDataRequest, Institution
from django.utils import timezone
import json
from django.contrib.auth.models import Group
from importlib import import_module
logger = logging.getLogger('dfva')


@login_required
def check_autorization(request):
    obj = get_object_or_404(UserConditionsAndTerms, user=request.user)
    if obj.signed:
        authorizationCM = import_module(settings.INSTITUION_AUTHORIZATION)
        auth = authorizationCM.authorize_user(request, request.user)
        if auth:
            group = Group.objects.get(name=settings.INSTITUTION_GROUP_NAME)
            request.user.groups.add(group)

    else:
        messages.warning(request, _(
            "User didn't sign the terms and conditions "))
    return redirect(reverse('home'))


@csrf_exempt
@require_POST
def sign_document_terms(request, pk):
    obj = get_object_or_404(UserConditionsAndTerms, pk=pk)

    signclient = ClienteFirmador(
        settings.DEFAULT_BUSSINESS,
        settings.DEFAULT_ENTITY)

    if signclient.validar_servicio():
        document = b64encode(obj.document_signed.encode())
        hash_sum = get_hash_sum(document, 'sha512')
        data = signclient.firme(
            request.user.username,
            document.decode(),
            'xml_cofirma',
            algoritmo_hash='Sha512',
            hash_doc=hash_sum,
            resumen="Acepta terminos de DFVA")

        signed_doc = SignDataRequest.objects.create(
            institution=Institution.objects.filter(
                administrative_institution=True).first(),
            notification_url='n/d',
            identification=request.user.username,
            request_datetime=timezone.now(),
            code=data['codigo_verificacion'],
            status=data['codigo_error'],
            status_text=data['texto_codigo_error'],
            expiration_datetime=timezone.now(
            ) - timezone.timedelta(int(data['tiempo_maximo'])),
            id_transaction=int(data['id_solicitud']),
            duration=data['tiempo_maximo'],
            document_format='xml'
        )
        request.session['signed_doc'] = signed_doc.pk
    else:
        logger.warning("Sign BCCR not available")
        data = signclient.DEFAULT_ERROR

    success = data['codigo_error'] == 1
    return JsonResponse({
        'FueExitosaLaSolicitud': success,
        'TiempoMaximoDeFirmaEnSegundos': 240,
        'TiempoDeEsperaParaConsultarLaFirmaEnSegundos': 2,
        'CodigoDeVerificacion': data['codigo_verificacion'],
        'IdDeLaSolicitud': data['id_solicitud'],
        'DebeMostrarElError': not success,
        'DescripcionDelError': data['texto_codigo_error'],

    })


def request_termsigned(request):
    callback = request.GET.get('callback')
    pk = request.GET.get('IdDeLaSolicitud', '')
    signdata = SignDataRequest.objects.filter(
        id_transaction=pk).first()

    sessionkey = None
    if 'signed_doc' in request.session:
        sessionkey = request.session['signed_doc']

    if signdata is None or signdata.pk != sessionkey:
        return HttpResponse(
            "%s(%s)" % (
                callback,
                json.dumps(
                    {"ExtensionData": {},
                     "DebeMostrarElError": True,
                     "DescripcionDelError": "Transacción inexistente",
                     "FueExitosa": False,
                     "SeRealizo": True}
                )
            )
        )

    status = signdata.status == 1
    realizada = signdata.received_notification
    if status and realizada:
        UserConditionsAndTerms.objects.filter(user=request.user).update(
            signed=True
        )
        request.session.pop('signed_doc')

    return HttpResponse(
        "%s(%s)" % (
            callback,
            json.dumps(
                {"ExtensionData": {},
                 "DebeMostrarElError": not status,
                 "DescripcionDelError": signdata.status_text,
                 "FueExitosa": status,
                 "SeRealizo": realizada}
            )
        )
    )


@login_required
@require_POST
def sign_terms(request):
    context = {}
    instance = UserConditionsAndTerms.objects.filter(user=request.user).first()

    form = UserConditionsAndTermsForm(
        request.POST, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        text = render_to_string(
            'terms_conditions/user_terms.html',
            context={'user': request.user,
                     'terms': instance}
        )
        context['text'] = text
        instance.text = text
        instance.document_signed = render_to_string(
            'terms_conditions/user_terms.xml',
            context={'user': request.user,
                     'terms': instance}
        )
        instance.user = request.user
        instance.save()
        context['object'] = instance
    else:
        messages.warning(request, _(
            'Request is invalid or incomplete, please try again'))
        return redirect(reverse('home'))

    return render(request, 'terms_conditions/sign_terms.html', context)