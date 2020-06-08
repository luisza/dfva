import json
from copy import copy
from urllib.parse import urlencode

from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Avg, Q, FloatField, Count, IntegerField
from django.template.defaultfilters import filesizeformat

from corebase.forms import StatForm
from pyfva.constants import ERRORES_AL_SOLICITAR_FIRMA
from datetime import timedelta
from django.utils.timezone import now
from corebase.models import System_Request_Metric
import random

def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = 'rgba(' + str(r) + ', ' + str(g) + ', ' + str(b) + ', 1)'
    return color

def get_filters(request):

    initials = {
        'start_date': now()+timedelta(days=-7),
        'end_date': now()
    }
    G = copy(request.GET)
    if 'start_date' not in G:
        G['start_date'] = now()+timedelta(days=-7)
    if 'end_date' not in G:
        G['end_date'] = now()
    form = StatForm(G)
    filter_dic = {}
    if form.is_valid():
        filter_dic['start_decrypt__gte'] = form.cleaned_data['start_date']
        filter_dic['start_decrypt__lte'] = form.cleaned_data['end_date']
        if form.cleaned_data['institution'] and form.cleaned_data['institution'] != 'None':
            filter_dic['institution__code'] = form.cleaned_data['institution']

       # filter_dic['transaction_success'] = form.cleaned_data['transaction_success']
    else:
         print(form)
    return filter_dic, form

@user_passes_test(lambda u: u.is_superuser)
def render_stats(request):
    query = System_Request_Metric.objects.all().order_by('start_decrypt')
    filters, form = get_filters(request)
    if filters:
        query = query.filter(**filters)

    alldata = System_Request_Metric.objects.all().order_by('start_decrypt')
    first_date = alldata.first().start_decrypt
    last_date = alldata.last().start_decrypt
    return render(request, 'base_stats.html', {
        'form':form,
        'form_params':  urlencode(form.to_dic_url()),
        'first_date': first_date,
        'last_date': last_date,
        'start_date': form.cleaned_data['start_date'],
        'end_date': form.cleaned_data['end_date']})


@user_passes_test(lambda u: u.is_superuser)
def get_durations_stats(request ):
    """
    Obtiene las estadísticas del systema

    :param request: Django request
    :return: Una respuesta JSON con los datos necesarios para crear un gráfico con Chartjs
    """

    datasets = {
        'bccr_call': {
            "label": 'Llamando al BCCR',
            "backgroundColor": get_random_color(),
            "data": []
        },
        'save_database': {
            "label": 'Guardando en base de datos',
            "backgroundColor": get_random_color(),
            "data": []
        },
        "check_institution_certificate": {
            "label": 'Comprobando certificados',
            "backgroundColor": get_random_color(),
            "data": []
        },
        "decrypt_time": {
            "label": 'Desencriptando',
            "backgroundColor": get_random_color(),
            "data": []
        },
        "encrypt_time": {
            "label": 'Encriptando',
            "backgroundColor": get_random_color(),
            "data": []
        },
        "total_spend_time": {
             "label": 'Total',
             "backgroundColor": get_random_color(),
             "data": []
         }
    }
    query = System_Request_Metric.objects.all()
    filters, form = get_filters(request)
    if filters:
        query = query.filter(**filters)

    names = ["Authentication", "Signer", "Validate Certificate", "Validate Document"]
    labels = ['Autenticación', 'Firma', 'Validación de certificado', 'Validación de documento']

    ops = {}
    extras = """<h3>Totales: Duración en segundos promedio </h3><table class="table"><thead class="thead-light">
    <tr> %s </tr></thead><tbody> %s </tbody> </table>"""
    extra_dev = ""
    for operation_type in names:
        key_opt = operation_type.lower().replace(" ", "")
        for key in datasets.keys():
            ops[key_opt+"_"+key] = Avg(key,
                                    filter=Q(operation_type=operation_type),
                                    output_field=FloatField())
    result = query.aggregate(**ops)
    for operation_type in names:
        key_opt = operation_type.lower().replace(" ", "")
        for key in datasets.keys():
            datasets[key]['data'].append(result[ key_opt + "_"+key] or 0 )

        extra_dev += "<td>%.2f</td>"%(result[key_opt + "_" + "total_spend_time"] or 0,)

    extras = extras%("".join(["<td>"+x+"</td>" for x in  labels]),
                     extra_dev)

    dev = {
        'chartid': request.GET.get('chartid'),
        'after_graph':'',
         'graph': {
             "type": 'bar',
             "data":{
                 'labels': labels,
                 'datasets': [datasets[x] for x in datasets if x != "total_spend_time"],
             },
             "options": {
                 "title": {
                     "display": True,
                     "text": 'Duración en segundos de peticiones'
                 },
                 "tooltips": {
                     "mode": 'index',
                     "intersect": False
                 },
                 "responsive": True,
                 "scales": {
                     "xAxes": [{
                         "stacked": True,
                     }],
                     "yAxes": [{
                         "stacked": True
                     }]
                 }
             }

         },
         'extras' : extras
    }

    return JsonResponse(dev)


@user_passes_test(lambda u: u.is_superuser)
def get_total_stats(request ):
    datasets = {
        'total': {
            "label": 'Total de peticiones hechas',
            "backgroundColor": get_random_color(),
            "data": []
        },

    }
    query = System_Request_Metric.objects.all()
    filters, form = get_filters(request)
    if filters:
        query = query.filter(**filters)

    ops = {}
    extras = """<h3>Total de peticiones realizadas</h3><table class="table"><thead class="thead-light">
    <tr> %s </tr></thead><tbody> %s </tbody> </table>"""
    extra_dev = ""
    labels = ['Autenticación', 'Firma', 'Validación de certificado', 'Validación de documento']
    ops = {}
    for operation_type in ["Authentication", "Signer", "Validate Certificate", "Validate Document"]:
        key_opt = operation_type.lower().replace(" ", "")
        for key in datasets.keys():
            ops[key_opt+"_"+key] = Count('id',
                                    filter=Q(operation_type=operation_type),
                                    output_field=FloatField())
    result = query.aggregate(**ops)
    for operation_type in ["Authentication", "Signer", "Validate Certificate", "Validate Document"]:
        key_opt = operation_type.lower().replace(" ", "")
        for key in datasets.keys():
            datasets[key]['data'].append(result[ key_opt + "_"+key] )
            extra_dev += "<td>%.2f</td>" % (result[key_opt + "_" + key] or 0,)

    extras = extras%("".join(["<td>"+x+"</td>" for x in labels]),
                     extra_dev)

    dev = {
        'chartid': request.GET.get('chartid'),
        'after_graph': '',
         'graph': {
             "type": 'bar',
             "data":{
                 'labels': labels,
                 'datasets': [datasets[x] for x in datasets  ],
             },
             "options": {
                 "title": {
                     "display": True,
                     "text": 'Total de peticiones'
                 },
                 "tooltips": {
                     "mode": 'index',
                     "intersect": False
                 },
                 "responsive": True,
                 "scales": {
                     "xAxes": [{
                         "stacked": True,
                     }],
                     "yAxes": [{
                         "stacked": True
                     }]
                 }
             }

         },
         'extras': extras
    }

    return JsonResponse(dev)


@user_passes_test(lambda u: u.is_superuser)
def get_error_stats(request ):
    """
    Obtiene las estadísticas del systema

    :param request: Django request
    :return: Una respuesta JSON con los datos necesarios para crear un gráfico con Chartjs
    """

    datasets = {

        "total": {
             "label": 'Total',
             "backgroundColor": get_random_color(),
             "data": []
         }
    }

    query = System_Request_Metric.objects.all()
    filters, form = get_filters(request)
    if filters:
        query = query.filter(**filters)
    extras = """<h3>Total de peticiones realizadas</h3><table class="table"><thead class="thead-light">
    <tr> %s </tr></thead><tbody> %s </tbody> </table>"""
    extra_dev = ""

    labels = []
    ops = {}
    for operation_type in ERRORES_AL_SOLICITAR_FIRMA:
        key_opt = str(operation_type[0])
        for key in datasets.keys():
            ops[key+"_"+key_opt] = Count('id',
                                    filter=Q(transaction_status=key_opt),
                                    output_field=IntegerField())
    result = query.aggregate(**ops)
    extra_label = []
    for operation_type in ERRORES_AL_SOLICITAR_FIRMA:
        key_opt = str(operation_type[0])
        for key in datasets.keys():
            if result[ key+"_"+key_opt] != 0 :
                labels.append(operation_type[0])
                extra_label.append("%d) %s\n"%(operation_type[0], operation_type[1]))
                datasets[key]['data'].append(result[ key+"_"+key_opt] )
                extra_dev += "<tr><td>%d</td> <td class=\"text-justify\" >%s</td>"%(operation_type[0], operation_type[1])
                extra_dev += "<td>%.2f</td></tr>" % (result[key+"_"+key_opt] or 0,)

    extras = extras%("<td>Código</td><td>Descripción</td><td>Total</td>",  extra_dev )
    dev = {
        'chartid': request.GET.get('chartid'),
        'after_graph': '<div class="text-justify">'+ '<br>'.join(extra_label)+"</div>",
         'graph': {
             "type": 'bar',
             "data":{
                 'labels': labels,
                 'datasets': [datasets[x] for x in datasets ],
             },
             "options": {
                 "title": {
                     "display": True,
                     "text": 'Estados de las peticiones'
                 },
                 "tooltips": {
                     "mode": 'index',
                     "intersect": False
                 },
                 "responsive": True,
                 "scales": {
                     "xAxes": [{
                         "stacked": True,
                         'scaleLabel': {
                             'display': True,

                         }
                     }],
                     "yAxes": [{
                         "stacked": True
                     }]
                 }
             }

         },
         'extras': extras
    }

    return JsonResponse(dev)



@user_passes_test(lambda u: u.is_superuser)
def get_size_stats(request ):
    """
    Obtiene las estadísticas del systema

    :param request: Django request
    :return: Una respuesta JSON con los datos necesarios para crear un gráfico con Chartjs
    """

    datasets = {
        'request_size': {
            "label": 'Tamaño promedio',
            "backgroundColor": get_random_color(),
            "data": []
        }
    }
    query = System_Request_Metric.objects.all()
    filters, form = get_filters(request)
    if filters:
        query = query.filter(**filters)

    names = ["Authentication", "Signer", "Validate Certificate", "Validate Document"]
    labels = ['Autenticación', 'Firma', 'Validación de certificado', 'Validación de documento']

    ops = {}
    extras = """<h3>Tamaño promedio </h3><table class="table"><thead class="thead-light">
    <tr> %s </tr></thead><tbody> %s </tbody> </table>"""
    extra_dev = ""
    for operation_type in names:
        key_opt = operation_type.lower().replace(" ", "")
        for key in datasets.keys():
            ops[key_opt+"_"+key] = Avg(key,
                                    filter=Q(operation_type=operation_type),
                                    output_field=FloatField())
    result = query.aggregate(**ops)
    for operation_type in names:
        key_opt = operation_type.lower().replace(" ", "")
        for key in datasets.keys():
            datasets[key]['data'].append(float(result[ key_opt + "_"+key] or 0)/1000  )
            extra_dev += "<td>"+filesizeformat( result[ key_opt + "_"+key] or 0  )+"</td>"
    extras = extras%("".join(["<td>"+x+"</td>" for x in labels]),
                     extra_dev)

    dev = {
        'chartid': request.GET.get('chartid'),
        'after_graph':'',
         'graph': {
             "type": 'bar',
             "data":{
                 'labels': labels,
                 'datasets': [datasets[x] for x in datasets],
             },
             "options": {
                 "title": {
                     "display": True,
                     "text": 'Tamaño promedio en KB'
                 },
                 "tooltips": {
                     "mode": 'index',
                     "intersect": False
                 },
                 "responsive": True,
                 "scales": {
                     "xAxes": [{
                         "stacked": True,
                     }],
                     "yAxes": [{
                         "stacked": True
                     }]
                 }
             }

         },
         'extras' : extras
    }

    return JsonResponse(dev)
