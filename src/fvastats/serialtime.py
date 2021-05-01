import random
from datetime import timedelta, datetime

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import render
from django.db.models.aggregates import Count

from corebase.models import System_Request_Metric
from fvastats.views import get_filters


def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = 'rgba(' + str(r) + ', ' + str(g) + ', ' + str(b) + ', 1)'
    return color

def get_the_value(value, default=0):
    try:
        p = int(value)
    except:
        p = default
    return p


@user_passes_test(lambda u: u.is_superuser)
def show_timeperminute(request):
    p = get_the_value(request.GET.get('p', '0'))
    c = get_the_value(request.GET.get('c', '20'), 20)

    ini = c*p
    fin = c*(p+1)

    query = System_Request_Metric.objects.all().order_by('start_decrypt')
    filters, form = get_filters(request)
    if filters:
        query = query.filter(**filters)
    dates_requested = query.datetimes(
        'start_decrypt',
        "minute"
    )
    pages = dates_requested.count()//c -1
    dates_requested = dates_requested[ini:fin]

    query_params = {}
    for d in  dates_requested:
        query_params[d.strftime( "f_%m_%d_%Y_%H_%M")] = Count('start_decrypt', filter=Q(
            start_decrypt__range=(d, d+timedelta(minutes=1))  ))
    result = query.aggregate(**query_params)
    data = [result[d.strftime( "f_%m_%d_%Y_%H_%M")] for d in  dates_requested]
    return render(request, 'stats_serialtime.html', {
        'dates_requested': dates_requested,
        'color': get_random_color(),
        'p': p,
        'c': c,
        'pages': pages,
        'data': data,
        'form': form
    })