# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-15 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_auto_20170913_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='validatepersoncertificaterequest',
            name='format',
            field=models.CharField(choices=[('cofirma', 'CoFirma'), ('contrafirma', 'ContraFirma'), ('msoffice', 'MS Office'), ('odf', 'Open Document Format')], default='n/d', max_length=15),
        ),
    ]
