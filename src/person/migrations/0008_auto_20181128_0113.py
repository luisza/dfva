# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-28 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0007_auto_20181114_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='authenticatepersondatarequest',
            name='hash_id_docsigned',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signpersondatarequest',
            name='hash_id_docsigned',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='authenticatepersondatarequest',
            name='hash_docsigned',
        ),
        migrations.RemoveField(
            model_name='signpersondatarequest',
            name='hash_docsigned',
        ),
        migrations.AddField(
            model_name='authenticatepersondatarequest',
            name='hash_docsigned',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='signpersondatarequest',
            name='hash_docsigned',
            field=models.TextField(blank=True, null=True),
        ),
    ]