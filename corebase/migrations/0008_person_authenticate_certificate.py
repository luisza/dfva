# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-04 04:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corebase', '0007_auto_20170813_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='authenticate_certificate',
            field=models.TextField(blank=True, null=True),
        ),
    ]