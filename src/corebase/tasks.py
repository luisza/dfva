import importlib

from django.core.mail import mail_admins

from corebase.models import BCCR_Monitor
from pyfva.clientes.autenticador import ClienteAutenticador
from pyfva.clientes.firmador import ClienteFirmador
from pyfva.clientes.validador import ClienteValidador
from django.utils import timezone
from django.conf import settings

app = importlib.import_module(settings.CELERY_MODULE).app
from corebase import logger

@app.task
def chek_bccr_service_status():
    authclient = ClienteAutenticador(settings.DEFAULT_BUSSINESS, settings.DEFAULT_ENTITY)
    signclient = ClienteFirmador(
        negocio=settings.DEFAULT_BUSSINESS,
        entidad=settings.DEFAULT_ENTITY,
    )
    clientvalida = ClienteValidador(settings.DEFAULT_BUSSINESS, settings.DEFAULT_ENTITY)

    metric ={
    'medition_time' : timezone.now(),
    'authenticate': authclient.validar_servicio(),
    'signer': signclient.validar_servicio(),
    'validate_certificate': clientvalida.validar_servicio('certificado'),
    'validate_document': clientvalida.validar_servicio('documento')
    }
    metric['everything_ok'] = all((metric['authenticate'], metric['signer'], metric['validate_certificate'],
                                   metric['validate_document']))

    BCCR_Monitor.objects.create(**metric)
    if not metric['everything_ok']:
        mdebug = dict(metric)
        mdebug['medition_time'] = metric['medition_time'].strftime("%m/%d/%Y, %H:%M:%S")
        logger.info({'message': "Check BCCR ", 'data':repr(mdebug), 'location': __file__})
        mail_admins(
            "Problemas de comunicación con el BCCR",
            "Informe de estado: "+repr(mdebug),
            fail_silently=True
        )
    return "%s %r"%(metric['medition_time'].strftime("%m/%d/%Y, %H:%M:%S"), metric['everything_ok'])

@app.task
def clean_ok_services_status():
    today = timezone.now()
    deleted_checks=0
    query = BCCR_Monitor.objects.filter(everything_ok=True, medition_time__week=today.isocalendar()[1],
                                medition_time__year=today.year)
    if query.exists():
        log_string=""
        for value in query.values():
            log_string = "%s %s %s %s %s %s\n"%(
                value['medition_time'].strftime("%m/%d/%Y, %H:%M:%S"),
                value['authenticate'],
                value['signer'],
                value['validate_certificate'],
                value['validate_document'],
                value['everything_ok']
            )
        logger.info({'message': "Eliminando Status check: ", 'data':log_string, 'location': __file__})
        deleted_checks = query.delete()[0]

    return  "Total status eliminados: "+str(deleted_checks)

