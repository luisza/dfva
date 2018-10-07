# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 17/7/2018
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''


from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from institution.models import AuthenticateDataRequest, InstitutionStats,\
    SignDataRequest, ValidateCertificateDataRequest, \
    ValidateDocumentDataRequest

from django.contrib.auth.management import create_permissions

from django.conf import settings


@receiver(post_migrate, )
def create_group(sender, **kwargs):
    apps = kwargs.get('apps')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    for app_config in apps.get_app_configs():
        if app_config.name == 'institution':
            app_config.models_module = True
            create_permissions(app_config, apps=apps, verbosity=0)
            app_config.models_module = None

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
            was_successfully=instance.status == 1
        )
    else:
        InstitutionStats.objects.filter(transaction_id=instance.pk,
                                        data_type=0).update(
            status=instance.status,
            notified=instance.received_notification,
            was_successfully=instance.status == 1
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
            was_successfully=instance.status == 1
        )
    else:
        InstitutionStats.objects.filter(transaction_id=instance.pk,
                                        data_type=1).update(
            status=instance.status,
            notified=instance.received_notification,
            was_successfully=instance.status == 1
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
            was_successfully=instance.was_successfully
        )
    else:
        InstitutionStats.objects.filter(transaction_id=instance.pk,
                                        data_type=2).update(
            status=instance.status,
            notified=True,
            was_successfully=instance.was_successfully
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
            was_successfully=instance.was_successfully
        )
    else:
        InstitutionStats.objects.filter(transaction_id=instance.pk,
                                        data_type=3).update(
            status=instance.status,
            notified=True,
            was_successfully=instance.was_successfully
        )
