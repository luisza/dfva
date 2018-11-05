# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='BaseDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertencias', models.ManyToManyField(to='corebase.Advertencia')),
            ],
        ),
        migrations.CreateModel(
            name='ErrorEncontrado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=250)),
                ('detalle', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Firmante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=25)),
                ('fecha_de_firma', models.DateField()),
                ('nombre_completo', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='basedocument',
            name='errores',
            field=models.ManyToManyField(to='corebase.ErrorEncontrado'),
        ),
        migrations.AddField(
            model_name='basedocument',
            name='firmantes',
            field=models.ManyToManyField(to='corebase.Firmante'),
        ),
    ]