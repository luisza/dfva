# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 02:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0002_auto_20170417_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticatedatarequest',
            name='identification',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^(\\d{9,11})$', message='Debe contener 9 dígitos o 11 para extranjeros y 10 para cédulas jurídicas por ejemplo: 102340456 para nacionales o 10234045611 para extranjeros')]),
        ),
        migrations.AlterField(
            model_name='authenticatedatarequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'Solicitud recibida correctamente'), (2, 'Ha ocurrido algún problema al solicitar la firma'), (3, 'Solicitud con campos incompletos'), (4, 'Diferencia de hora no permitida entre cliente y servidor'), (5, 'La entidad no se encuentra registrada'), (6, 'La entidad se encuentra en estado inactiva'), (7, 'La URL no pertenece a la entidad solicitante'), (8, 'El tamaño de hash debe ser entre 1 y 130 caracteres'), (9, 'Algoritmo desconocido'), (10, 'Certificado incorrecto')], default=1),
        ),
    ]
