# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-10 03:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0010_auto_20180618_0536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='institutionstats',
            old_name='fue_exitosa',
            new_name='was_successfully',
        ),
        migrations.RenameField(
            model_name='validatecertificatedatarequest',
            old_name='fin_vigencia',
            new_name='end_validity',
        ),
        migrations.RenameField(
            model_name='validatecertificatedatarequest',
            old_name='nombre_completo',
            new_name='full_name',
        ),
        migrations.RenameField(
            model_name='validatecertificatedatarequest',
            old_name='inicio_vigencia',
            new_name='start_validity',
        ),
        migrations.RenameField(
            model_name='validatecertificatedatarequest',
            old_name='fue_exitosa',
            new_name='was_successfully',
        ),
        migrations.RenameField(
            model_name='validatedocumentdatarequest',
            old_name='fue_exitosa',
            new_name='was_successfully',
        ),
    ]