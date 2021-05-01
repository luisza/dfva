from django.db.models import Count, Avg, Q
from dateutil.relativedelta import relativedelta

def create_summary(DataSummary, System_Request_Metric, last_month,  this_month):
    objs = System_Request_Metric.objects.filter(start_decrypt__range=(last_month, this_month))

    # operation_type ["Authentication", "Signer", "Validate Certificate", "Validate Document"]
    query = objs.aggregate(
        total_number_of_records=Count('pk'),
        authentication_total=Count('pk', filter=Q(operation_type="Authentication")),
        signer_total=Count('pk', filter=Q(operation_type="Signer")),
        validatecertificate_total=Count('pk', filter=Q(operation_type="Validate Certificate")),
        validatedocument_total=Count('pk', filter=Q(operation_type="Validate Document")),
        authentication_total_spend_time=Avg('total_spend_time', filter=Q(operation_type="Authentication")),
        signer_total_spend_time=Avg('total_spend_time', filter=Q(operation_type="Signer")),
        validatecertificate_total_spend_time=Avg('total_spend_time', filter=Q(operation_type="Validate Certificate")),
        validatedocument_total_spend_time=Avg('total_spend_time', filter=Q(operation_type="Validate Document")),

        authentication_request_size=Avg('request_size', filter=Q(operation_type="Authentication")),
        signer_request_size=Avg('request_size', filter=Q(operation_type="Signer")),
        validatecertificate_request_size=Avg('request_size', filter=Q(operation_type="Validate Certificate")),
        validatedocument_request_size=Avg('request_size', filter=Q(operation_type="Validate Document")),
    )

    sumary = DataSummary.objects.create(
        month="%02d"%last_month.month,
        year=last_month.year,
        total_number_of_records=query['total_number_of_records'],
        # Promedio de duraciones de acuerdo al mes y al año
        authentication_total=query['authentication_total'] or 0,
        signer_total=query['signer_total'] or 0,
        validatecertificate_total=query['validatecertificate_total'] or 0,
        validatedocument_total=query['validatedocument_total'] or 0,
        authentication_total_spend_time=query['authentication_total_spend_time'] or 0,
        signer_total_spend_time=query['signer_total_spend_time'] or 0,
        validatecertificate_total_spend_time=query['validatecertificate_total_spend_time'] or 0,
        validatedocument_total_spend_time=query['validatedocument_total_spend_time'] or 0,
        authentication_request_size=query['authentication_request_size'] or 0,
        signer_request_size=query['signer_request_size'] or 0,
        validatecertificate_request_size=query['validatecertificate_request_size'] or 0,
        validatedocument_request_size=query['validatedocument_request_size'] or 0
    )

    return objs, query, sumary


def create_summary_between_dates(DataSummary, System_Request_Metric):
    ifirst = System_Request_Metric.objects.order_by('start_decrypt').first()
    ilast = System_Request_Metric.objects.order_by('start_decrypt').last()
    startdate = ifirst.start_decrypt + relativedelta(months=+1)
    lastdate = ilast.start_decrypt
    actual = startdate
    while actual < lastdate:
        this_month = actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month = this_month + relativedelta(months=-1)
        create_summary(DataSummary, System_Request_Metric, last_month,  this_month)
        actual = this_month + relativedelta(months=+1)