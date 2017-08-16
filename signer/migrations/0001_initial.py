# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 22:04
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corebase', '0003_auto_20170719_0547'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignDataRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_url', models.URLField()),
                ('identification', models.CharField(help_text="'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'", max_length=15, validators=[django.core.validators.RegexValidator('^(\\d{9,11})$', message='Debe contener 9 dígitos o 11 para extranjeros y 10 para cédulas jurídicas por ejemplo: 102340456 para nacionales o 10234045611 para extranjeros')])),
                ('request_datetime', models.DateTimeField()),
                ('code', models.CharField(default='N/D', max_length=20)),
                ('status', models.IntegerField(choices=[(1, 'Solicitud recibida correctamente'), (2, 'Ha ocurrido algún problema al solicitar la firma'), (3, 'Solicitud con campos incompletos'), (4, 'Diferencia de hora no permitida entre cliente y servidor'), (5, 'La entidad no se encuentra registrada'), (6, 'La entidad se encuentra en estado inactiva'), (7, 'La URL no pertenece a la entidad solicitante'), (8, 'El tamaño de hash debe ser entre 1 y 130 caracteres'), (9, 'Algoritmo desconocido'), (10, 'Certificado incorrecto')], default=1)),
                ('response_datetime', models.DateTimeField(auto_now=True)),
                ('expiration_datetime', models.DateTimeField()),
                ('id_transaction', models.IntegerField(default=0)),
                ('sign_document', models.TextField(blank=True, null=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corebase.Institution')),
            ],
            options={
                'permissions': (('view_signerdatarequest', 'Can see available Signer Data Request'),),
                'ordering': ('request_datetime',),
            },
        ),
        migrations.CreateModel(
            name='SignRequest',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('arrived_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('data_hash', models.CharField(help_text='Suma hash de datos de tamaño máximo 130 caracteres, usando el\n                                 algoritmo especificado ', max_length=130)),
                ('algorithm', models.CharField(choices=[('sha256', 'sha256'), ('sha384', 'sha384'), ('sha512', 'sha512')], help_text=' Debe ser alguno de los siguientes: sha256, sha384, sha512', max_length=7)),
                ('public_certificate', models.TextField(help_text='Certificado público de la institución (ver Institución) ')),
                ('institution', models.CharField(help_text='UUID de la institución', max_length=50)),
                ('data_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='signer.SignDataRequest')),
            ],
            options={
                'permissions': (('view_signrequest', 'Can see available Sign Request'),),
                'ordering': ('arrived_time',),
            },
        ),
    ]