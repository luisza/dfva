# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-01 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorFound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=250)),
                ('detail', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Signer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification_number', models.CharField(max_length=25)),
                ('signature_date', models.DateField()),
                ('full_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='WarningReceived',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=512)),
            ],
        ),
    ]
