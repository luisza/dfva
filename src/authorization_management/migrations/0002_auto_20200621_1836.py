# Generated by Django 3.0.7 on 2020-06-22 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconditionsandterms',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
    ]