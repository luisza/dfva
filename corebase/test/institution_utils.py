'''
Created on 15 ago. 2017

@author: luis
'''

from corebase.ca_management import create_certiticate
from institution.models import Institution, NotificationURL


def create_institution(user, domain='dfva.cr',
                       name="test institution",
                       institution_unit='QA'):
    save_model = Institution(
        user=user,
        name=name,
        active=True,
        domain=domain,
        institution_unit=institution_unit)
    create_certiticate(domain, save_model)
    save_model.save()

    return save_model


def create_url(institution, url='N/D', description="test url", is_demo=False):
    return NotificationURL.objects.create(
        description=description,
        url=url,
        institution=institution,
        not_webapp=url == 'N/D',
        is_demo=is_demo
    )
