'''
@date: 21/06/2020
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from corebase.ca_management import create_certiticate
from institution.models import Institution


class Command(BaseCommand):
    help = 'Crea una institución base'

    def create_institution(self, user, domain='dfva.cr',
                           name="master institution",
                           institution_unit='QA'):


        save_model = Institution(
            user=user,
            name=name,
            active=True,
            domain=domain,
            institution_unit=institution_unit,
            administrative_institution=True
        )
        create_certiticate(domain, save_model)
        save_model.save()

        return save_model

    def handle(self, *args, **options):
        user = User.objects.filter(is_superuser=True, is_active=True).first()
        if user is None:
            print("Necesita crear un usuario administrador")
            return 1
        institution = Institution.objects.filter(administrative_institution=True).first()
        if institution is not None:
            print("Institución administrativa ya fue creada")
            return 1

        self.create_institution(user)