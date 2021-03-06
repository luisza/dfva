# Generated by Django 3.0.7 on 2020-07-19 23:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import person.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corebase', '0003_auto_20200609_0020'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('identification', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('expiration_datetime_token', models.DateTimeField(blank=True, null=True)),
                ('last_error_code', models.SmallIntegerField(choices=[(1, 'Transacción satisfactoria'), (2, 'Error, persona no existe'), (3, 'Error no determinado')], default=1)),
                ('authenticate_certificate', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrived_time', models.DateTimeField(auto_now_add=True)),
                ('public_certificate', models.TextField(help_text='Certificado público  de firma, para firma digital avanzada')),
                ('code', models.TextField()),
                ('person', models.CharField(help_text='Identificación de la persona solicitante', max_length=50)),
                ('data_hash', models.CharField(help_text='Suma hash de datos de tamaño máximo 130 caracteres, usando el\n                                 algoritmo especificado ', max_length=130)),
                ('algorithm', models.CharField(choices=[('sha256', 'sha256'), ('sha384', 'sha384'), ('sha512', 'sha512')], help_text=' Debe ser alguno de los siguientes: sha256, sha384, sha512', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='ValidatePersonDocumentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_datetime', models.DateTimeField()),
                ('code', models.CharField(default='N/D', max_length=40)),
                ('format', models.CharField(choices=[('cofirma', 'CoFirma'), ('contrafirma', 'ContraFirma'), ('msoffice', 'MS Office'), ('odf', 'Open Document Format'), ('pdf', 'PDF')], default='n/d', max_length=15)),
                ('status', models.IntegerField(default=0)),
                ('status_text', models.CharField(default='n/d', max_length=256)),
                ('was_successfully', models.BooleanField(default=True)),
                ('arrived_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('document', models.TextField()),
                ('response_datetime', models.DateTimeField()),
                ('errors', models.ManyToManyField(to='corebase.ErrorFound')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
                ('signers', models.ManyToManyField(to='corebase.Signer')),
                ('warnings', models.ManyToManyField(to='corebase.WarningReceived')),
            ],
            options={
                'ordering': ('arrived_time',),
            },
        ),
        migrations.CreateModel(
            name='ValidatePersonCertificateRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_datetime', models.DateTimeField()),
                ('code', models.CharField(default='N/D', max_length=20)),
                ('status', models.IntegerField(choices=[(0, 'Solicitud recibida correctamente'), (1, 'Ha ocurrido algún problema al solicitar la firma'), (2, 'Solicitud con campos incompletos'), (3, 'Diferencia de hora no permitida entre cliente y servidor'), (4, 'La entidad no se encuentra registrada'), (5, 'La entidad se encuentra en estado inactiva'), (6, 'La URL no pertenece a la entidad solicitante'), (7, 'El tamaño de hash debe ser entre 1 y 130 caracteres'), (8, 'Algoritmo desconocido'), (9, 'Certificado incorrecto')], default=0)),
                ('status_text', models.CharField(default='n/d', max_length=256)),
                ('response_datetime', models.DateTimeField(auto_now=True)),
                ('expiration_datetime', models.DateTimeField(default=person.models.get_default_expiration)),
                ('identification', models.CharField(blank=True, help_text="'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'", max_length=15, null=True)),
                ('arrived_time', models.DateTimeField(auto_now_add=True)),
                ('was_successfully', models.BooleanField(default=True)),
                ('full_name', models.CharField(max_length=250, null=True)),
                ('start_validity', models.DateTimeField(null=True)),
                ('end_validity', models.DateTimeField(null=True)),
                ('document', models.TextField()),
                ('format', models.CharField(max_length=20)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
            ],
            options={
                'ordering': ('arrived_time',),
            },
        ),
        migrations.CreateModel(
            name='SignPersonRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_datetime', models.DateTimeField()),
                ('code', models.CharField(default='N/D', max_length=20)),
                ('status', models.IntegerField(choices=[(0, 'Solicitud recibida correctamente'), (1, 'Ha ocurrido algún problema al solicitar la firma'), (2, 'Solicitud con campos incompletos'), (3, 'Diferencia de hora no permitida entre cliente y servidor'), (4, 'La entidad no se encuentra registrada'), (5, 'La entidad se encuentra en estado inactiva'), (6, 'La URL no pertenece a la entidad solicitante'), (7, 'El tamaño de hash debe ser entre 1 y 130 caracteres'), (8, 'Algoritmo desconocido'), (9, 'Certificado incorrecto')], default=0)),
                ('status_text', models.CharField(default='n/d', max_length=256)),
                ('response_datetime', models.DateTimeField(auto_now=True)),
                ('expiration_datetime', models.DateTimeField(default=person.models.get_default_expiration)),
                ('identification', models.CharField(help_text="'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'", max_length=15, validators=[django.core.validators.RegexValidator('(^[1|5]\\d{11}$)|(^\\d{2}-\\d{4}-\\d{4}$)', message='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000')])),
                ('id_transaction', models.IntegerField(default=0)),
                ('signed_document', models.TextField(blank=True, null=True)),
                ('duration', models.SmallIntegerField(default=3)),
                ('received_notification', models.BooleanField(default=False)),
                ('hash_docsigned', models.TextField(blank=True, null=True)),
                ('hash_id_docsigned', models.SmallIntegerField(default=0)),
                ('arrived_time', models.DateTimeField(auto_now_add=True)),
                ('document', models.TextField()),
                ('format', models.CharField(max_length=15)),
                ('algorithm_hash', models.CharField(max_length=50)),
                ('document_hash', models.TextField()),
                ('resume', models.CharField(max_length=500)),
                ('public_certificate', models.TextField(help_text='Certificado público  de firma, para firma digital avanzada')),
                ('place', models.CharField(blank=True, max_length=256, null=True)),
                ('reason', models.CharField(blank=True, max_length=256, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
            ],
            options={
                'ordering': ('arrived_time',),
            },
        ),
        migrations.CreateModel(
            name='AuthenticatePersonRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_datetime', models.DateTimeField()),
                ('code', models.CharField(default='N/D', max_length=20)),
                ('status', models.IntegerField(choices=[(0, 'Solicitud recibida correctamente'), (1, 'Ha ocurrido algún problema al solicitar la firma'), (2, 'Solicitud con campos incompletos'), (3, 'Diferencia de hora no permitida entre cliente y servidor'), (4, 'La entidad no se encuentra registrada'), (5, 'La entidad se encuentra en estado inactiva'), (6, 'La URL no pertenece a la entidad solicitante'), (7, 'El tamaño de hash debe ser entre 1 y 130 caracteres'), (8, 'Algoritmo desconocido'), (9, 'Certificado incorrecto')], default=0)),
                ('status_text', models.CharField(default='n/d', max_length=256)),
                ('response_datetime', models.DateTimeField(auto_now=True)),
                ('expiration_datetime', models.DateTimeField(default=person.models.get_default_expiration)),
                ('identification', models.CharField(help_text="'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'", max_length=15, validators=[django.core.validators.RegexValidator('(^[1|5]\\d{11}$)|(^\\d{2}-\\d{4}-\\d{4}$)', message='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000')])),
                ('id_transaction', models.IntegerField(default=0)),
                ('signed_document', models.TextField(blank=True, null=True)),
                ('duration', models.SmallIntegerField(default=3)),
                ('received_notification', models.BooleanField(default=False)),
                ('hash_docsigned', models.TextField(blank=True, null=True)),
                ('hash_id_docsigned', models.SmallIntegerField(default=0)),
                ('arrived_time', models.DateTimeField(auto_now_add=True)),
                ('public_certificate', models.TextField(help_text='Certificado público  de firma, para firma digital avanzada')),
                ('document_hash', models.TextField()),
                ('resume', models.CharField(max_length=500)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
            ],
            options={
                'ordering': ('arrived_time',),
            },
        ),
    ]
