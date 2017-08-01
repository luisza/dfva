from django.db import models
from corebase.models import NotificationURL

# Create your models here.


class Autenticar(models.Model):
    url = models.ForeignKey(NotificationURL)
