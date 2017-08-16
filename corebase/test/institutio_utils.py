'''
Created on 15 ago. 2017

@author: luis
'''
from corebase.models import Institution, NotificationURL
from corebase.ca_management import gen_cert
import os
from django.conf import settings


def create_institution(user, domain='dfva.cr',
                       name="test institution",
                       institution_unit='QA'):
    save_model = Institution(
        user=user,
        name=name,
        active=True,
        domain=domain,
        institution_unit=institution_unit)
    gen_cert(domain,
             save_model,
             os.path.join(
                 settings.CA_PATH, "ca_cert.pem"),
             os.path.join(settings.CA_PATH, "ca_key.pem")
             )

    save_model.save()

    return save_model


def create_url(institution, url='N/D', description="test url"):
    return NotificationURL.objects.create(
        description=description,
        url=url,
        institution=institution,
        not_webapp=url == 'N/D'
    )
