from django.db import models
from institution.models import NotificationURL


# Create your models here.


class Autenticar(models.Model):
    url = models.ForeignKey(NotificationURL)
