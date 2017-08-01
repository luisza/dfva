from django.db import models
from corebase.presentation import PEMpresentation
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid

from django.conf import settings

identification_validator = RegexValidator(
    r'^(\d{9,11})$',
    message="Debe contener 9 dígitos o 11 para extranjeros y 10 para cédulas jurídicas por ejemplo: 102340456 para "
            "nacionales o 10234045611 para extranjeros")

ALGORITHM = (
    ('sha256', 'sha256'),
    ('sha384', 'sha384'),
    ('sha512', 'sha512')
)


class Institution(models.Model, PEMpresentation):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250)
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    bccr_bussiness = models.IntegerField(default=settings.DEFAULT_BUSSINESS)
    bccr_entity = models.IntegerField(default=settings.DEFAULT_ENTITY)

    domain = models.CharField(max_length=250)  # Certificate domain
    institution_unit = models.CharField(
        max_length=250, default="ND")  # UO in cert
    private_key = models.TextField()
    public_key = models.TextField()
    public_certificate = models.TextField()
    server_sign_key = models.TextField()
    server_public_key = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pk',)
        permissions = (
            ("view_institution", "Can see available tasks"),
        )


class NotificationURL(models.Model):
    description = models.CharField(max_length=250)
    url = models.URLField(null=True, blank=True)
    institution = models.ForeignKey(Institution)
    not_webapp = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (
            self.institution.name,
            self.url or 'N/D'
        )

    class Meta:
        ordering = ('institution',)
        permissions = (
            ("view_notificationurl", "Can see available notification urls"),
        )


class Person(models.Model):
    user = models.OneToOneField(User)
    identification = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.user.get_full_name() or self.indentification
