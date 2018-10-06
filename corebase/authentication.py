'''
Created on 16 jun. 2018

@author: luis
'''
from django.http.response import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pyfva.clientes.autenticador import ClienteAutenticador
from django.conf import settings
import logging
from django.views.decorators.http import require_http_methods
import json
from institution.models import AuthenticateDataRequest, Institution
from django.utils import timezone
from django.contrib.auth import authenticate, login

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


@csrf_exempt
@require_http_methods(["POST"])
def login_with_bccr(request):
    identification = request.POST.get('Identificacion', '')
    if identification:
        authclient = ClienteAutenticador(settings.DEFAULT_BUSSINESS,
                                         settings.DEFAULT_ENTITY)
        if authclient.validar_servicio():
            data = authclient.solicitar_autenticacion(
                identification)

        else:
            logger.warning("Auth BCCR not available")
            data = authclient.DEFAULT_ERROR

        obj = AuthenticateDataRequest.objects.create(
            institution=Institution.objects.filter(
                administrative_institution=True).first(),
            notification_url='N/D',
            identification=identification,
            request_datetime=timezone.now(),
            code=data['codigo_verificacion'],
            status=data['codigo_error'],
            status_text=data['texto_codigo_error'],
            expiration_datetime=timezone.now(
            ) - timezone.timedelta(int(data['tiempo_maximo'])),
            id_transaction=int(data['id_solicitud']),
            duration=data['tiempo_maximo']
        )

        request.session['authenticatedata'] = obj.pk

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

    return Http404()


def consute_firma(request):
    callback = request.GET.get('callback')
    pk = request.GET.get('IdDeLaSolicitud', '')
    authdata = AuthenticateDataRequest.objects.filter(
        id_transaction=pk).first()

    sessionkey = None
    if 'authenticatedata' in request.session:
        sessionkey = request.session['authenticatedata']

    if authdata is None or authdata.pk != sessionkey:
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

    status = authdata.status == 1
    realizada = authdata.received_notification
    if status and realizada:
        request.session.pop('authenticatedata')
        user = authenticate(token=pk)
        if user is not None:
            login(request, user)
    return HttpResponse(
        "%s(%s)" % (
            callback,
            json.dumps(
                {"ExtensionData": {},
                 "DebeMostrarElError": not status,
                 "DescripcionDelError": authdata.status_text,
                 "FueExitosa": status,
                 "SeRealizo": realizada}
            )
        )
    )
