import csv
import importlib
import os
import zipfile

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now

from corebase.models import System_Request_Metric, DataSummary
from fvastats.utils import create_summary

app = importlib.import_module(settings.CELERY_MODULE).app


def export_system_metrics_to_csv(year, month, data):
    new_file = 'metrics_{}_{}.csv'.format(year, month)
    file_headers = [field.name for field in System_Request_Metric._meta.fields]
    with open(new_file, 'w') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(file_headers)
        csv_file.writerows([record.values() for record in data.values()])
    
    return new_file


def send_email_with_deleted_data(csv_file, sumary):
    subject = 'UCR-FVA Métricas del mes'
    body = render_to_string('email_stats.html', context={'sumary': sumary})
    to_email = settings.DATA_STAT_NOTIFY_EMAIL
    email_from = settings.DEFAULT_FROM_EMAIL

    # Compresses the csv file that will be attached to an email
    new_zip_file = csv_file.replace('.csv','.zip')
    zip_file = zipfile.ZipFile(new_zip_file, 'w')
    zip_file.write(csv_file, compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()

    with open(new_zip_file, 'rb') as zip_file:
        # Creates the email to send it
        email = EmailMessage(subject, body , email_from, to_email)
        email.content_subtype = 'html'
        email.attach(new_zip_file, zip_file.read(), 'application/zip')
        email.send(fail_silently=False)

    if os.path.exists(new_zip_file):
        os.remove(new_zip_file)


def calculate_month_metrics(last_month, this_month, send_email=True):
    objs, query, sumary = create_summary(DataSummary, System_Request_Metric, last_month,  this_month)

    if send_email:
        csv_name = export_system_metrics_to_csv(last_month.year, last_month.month, objs)
        send_email_with_deleted_data(csv_name, sumary)

        if os.path.exists(csv_name):
            os.remove(csv_name)


@app.task
def send_month_notification():
    this_month = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month = this_month + relativedelta(months=-1)
    calculate_month_metrics(last_month, this_month)