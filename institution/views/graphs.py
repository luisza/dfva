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
    was_successfully = []
    no_was_successfully = []
    was_successfully_notify = []
    no_was_successfully_notify = []

    for name, dtype in (
        ('Autenticación', 0),
        ('Firma', 1),
        ('Validación de certificado', 2),
        ('Validación de documento', 3)
    ):

        was_successfully.append({
            'x': name,
            'y': institution.institutionstats_set.filter(
                was_successfully=True,
                data_type=dtype,
            ).count()
        }
        )
        no_was_successfully.append({
            'x': name,
            'y': institution.institutionstats_set.filter(
                was_successfully=False,
                data_type=dtype,
            ).count()})

        was_successfully_notify.append({
            'x': name,
            'y':  institution.institutionstats_set.filter(
                was_successfully=True,
                data_type=dtype,
                notified=True
            ).count()})

        no_was_successfully_notify.append({
            'x': name,
            'y': institution.institutionstats_set.filter(
                was_successfully=False,
                data_type=dtype,
                notified=False
            ).count()})

    data.append({
                'label': "Exitosa",
                'borderColor': 'rgb(120, 38, 255)',
                'backgroundColor': 'rgb(120, 38, 255)',
                "fill": False,
                'data': was_successfully
                })

    data.append({
                'label': "No exitosa",
                'borderColor': 'rgb(153, 153, 184)',
                'backgroundColor': 'rgb(153, 153, 184)',
                "fill": False,
                'data': no_was_successfully
                })

    data.append({
                'label': "Exitosa y notificada",
                'borderColor': 'rgb(255, 205, 38)',
                'backgroundColor': 'rgba(255, 205, 38)',
                "fill": False,
                'data': was_successfully_notify
                })

    data.append({
                'label': "No exitosa y notificada",
                'borderColor': 'rgb(133, 38, 20)',
                'backgroundColor': 'rgba(133, 38, 20)',
                "fill": False,
                'data': no_was_successfully_notify
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
