'''
Created on 18 jun. 2018

@author: luis
'''
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import JsonResponse
from institution.models import Institution


@login_required
@permission_required('institution.change_institution')
def get_institution_stats(request, pk):
    institution = get_object_or_404(Institution, pk=pk)
    data = []
    fue_exitosa = []
    no_fue_exitosa = []
    fue_exitosa_notify = []
    no_fue_exitosa_notify = []

    for name, dtype in (
        ('Autenticación', 0),
        ('Firma', 1),
        ('Validación de certificado', 2),
        ('Validación de documento', 3)
    ):

        fue_exitosa.append({
            'x': name,
            'y': institution.institutionstats_set.filter(
                fue_exitosa=True,
                data_type=dtype,
            ).count()
        }
        )
        no_fue_exitosa.append({
            'x': name,
            'y': institution.institutionstats_set.filter(
                fue_exitosa=False,
                data_type=dtype,
            ).count()})

        fue_exitosa_notify.append({
            'x': name,
            'y':  institution.institutionstats_set.filter(
                fue_exitosa=True,
                data_type=dtype,
                notified=True
            ).count()})

        no_fue_exitosa_notify.append({
            'x': name,
            'y': institution.institutionstats_set.filter(
                fue_exitosa=False,
                data_type=dtype,
                notified=False
            ).count()})

    data.append({
                'label': "Exitosa",
                'borderColor': 'rgb(120, 38, 255)',
                'backgroundColor': 'rgb(120, 38, 255)',
                "fill": False,
                'data': fue_exitosa
                })

    data.append({
                'label': "No exitosa",
                'borderColor': 'rgb(153, 153, 184)',
                'backgroundColor': 'rgb(153, 153, 184)',
                "fill": False,
                'data': no_fue_exitosa
                })

    data.append({
                'label': "Exitosa y notificada",
                'borderColor': 'rgb(255, 205, 38)',
                'backgroundColor': 'rgba(255, 205, 38)',
                "fill": False,
                'data': fue_exitosa_notify
                })

    data.append({
                'label': "No exitosa y notificada",
                'borderColor': 'rgb(133, 38, 20)',
                'backgroundColor': 'rgba(133, 38, 20)',
                "fill": False,
                'data': no_fue_exitosa_notify
                })

    dev = {
        'chartid': request.GET.get('chartid'),
        'title': "Peticiones efectuadas",
        'axisY': "Peticiones",
        'data': data,
        'labels': ['Autenticación',
                   'Firma',
                   'Val. certificado',
                   'Val. documento'],
    }

    return JsonResponse(dev)
