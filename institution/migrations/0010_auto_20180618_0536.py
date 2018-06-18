# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-18 05:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0009_create_institution'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('notified', models.BooleanField(default=False)),
                ('transaction_id', models.IntegerField()),
                ('data_type', models.SmallIntegerField(choices=[(0, 'Autenticación'), (1, 'Firma'), (2, 'Validación de certificado'), (3, 'Validación de documento')])),
                ('document_type', models.CharField(default='n/d', max_length=15)),
                ('fue_exitosa', models.BooleanField(default=False)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institution.Institution')),
            ],
        ),
        migrations.AddField(
            model_name='signdatarequest',
            name='document_format',
            field=models.CharField(default='n/d', max_length=25),
        ),
        migrations.AlterField(
            model_name='authenticatedatarequest',
            name='identification',
            field=models.CharField(help_text='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000', max_length=15, validators=[django.core.validators.RegexValidator('"(^[1|5]\\d{11}$)|(^\\d{2}-\\d{4}-\\d{4}$)"', message='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000')]),
        ),
        migrations.AlterField(
            model_name='authenticatedatarequest',
            name='request_datetime',
            field=models.DateTimeField(help_text="'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'"),
        ),
        migrations.AlterField(
            model_name='signdatarequest',
            name='identification',
            field=models.CharField(help_text='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000', max_length=15, validators=[django.core.validators.RegexValidator('"(^[1|5]\\d{11}$)|(^\\d{2}-\\d{4}-\\d{4}$)"', message='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000')]),
        ),
        migrations.AlterField(
            model_name='signdatarequest',
            name='request_datetime',
            field=models.DateTimeField(help_text="'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'"),
        ),
        migrations.AlterField(
            model_name='validatecertificatedatarequest',
            name='identification',
            field=models.CharField(help_text='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000', max_length=15, null=True, validators=[django.core.validators.RegexValidator('"(^[1|5]\\d{11}$)|(^\\d{2}-\\d{4}-\\d{4}$)"', message='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000')]),
        ),
        migrations.AlterField(
            model_name='validatecertificatedatarequest',
            name='request_datetime',
            field=models.DateTimeField(help_text="'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'"),
        ),
    ]
