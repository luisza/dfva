'''
Created on 17 jun. 2018

@author: luis
'''

from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from institution.models import AuthenticateDataRequest, InstitutionStats,\
    SignDataRequest, ValidateCertificateDataRequest, ValidateDocumentDataRequest

from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from django.conf import settings


@receiver(post_migrate, )
def create_group(sender, **kwargs):
    apps = kwargs.get('apps')
    schema_editor = kwargs.get("schema_editor")
    for app_config in apps.get_app_configs():
        create_permissions(app_config, apps=apps, verbosity=0)

    group, created = Group.objects.get_or_create(
        name=settings.INSTITUTION_GROUP_NAME)
    if created:
        for perm in ['add_institution', 'change_institution', 'delete_institution']:
            add_thing = Permission.objects.get(codename=perm)
            group.permissions.add(add_thing)
        group.save()


@receiver(post_save, sender=AuthenticateDataRequest)
def create_auth_stats(sender, instance, created, **kwargs):
    if created:
        InstitutionStats.objects.create(
            institution=instance.institution,
            status=instance.status,
            notified=instance.received_notification,
            transaction_id=instance.pk,
            data_type=0,
            document_type="authentication",
            fue_exitosa=instance.status == 1
        )
    else:
        InstitutionStats.objects.filter(transaction_id=instance.pk,
                                        data_type=0).update(
            status=instance.status,
            notified=instance.received_notification,
            fue_exitosa=instance.status == 1
        )


@receiver(post_save, sender=SignDataRequest)
def create_sign_stats(sender, instance, created, **kwargs):
    if created:
        InstitutionStats.objects.create(
            institution=instance.institution,
            status=instance.status,
            notified=instance.received_notification,
            transaction_id=instance.pk,
            data_type=1,
            document_type=instance.document_format,
            fue_exitosa=instance.status == 1
        )
    else:
        InstitutionStats.objects.filter(transaction_id=instance.pk,
                                        data_type=1).update(
            status=instance.status,
            notified=instance.received_notification,
            fue_exitosa=instance.status == 1
        )


@receiver(post_save, sender=ValidateCertificateDataRequest)
def create_validatecertificate_stats(sender, instance, created, **kwargs):
    if created:
        InstitutionStats.objects.create(
            institution=instance.institution,
            status=instance.status,
            notified=True,
            transaction_id=instance.pk,
            data_type=2,
            document_type='certificate',
            fue_exitosa=instance.fue_exitosa
        )
    else:
        InstitutionStats.objects.filter(transaction_id=instance.pk,
                                        data_type=2).update(
            status=instance.status,
            notified=True,
            fue_exitosa=instance.fue_exitosa
        )


@receiver(post_save, sender=ValidateDocumentDataRequest)
def create_validatedocument_stats(sender, instance, created, **kwargs):
    if created:
        InstitutionStats.objects.create(
            institution=instance.institution,
            status=instance.status,
            notified=True,
            transaction_id=instance.pk,
            data_type=3,
            document_type=instance.format,
            fue_exitosa=instance.fue_exitosa
        )
    else:
        InstitutionStats.objects.filter(transaction_id=instance.pk,
                                        data_type=3).update(
            status=instance.status,
            notified=True,
            fue_exitosa=instance.fue_exitosa
        )
