
from django.conf import settings
import logging
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)
from django.db import models

class DJLogEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.Model):
            return str(obj)
        elif isinstance(obj, Exception):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode()
        return super().default(obj)


def info(data, sector=None):
    if sector is not None:
        data['sector'] = sector
    logger.info(
        json.dumps(data, cls=DJLogEncoder)
    )

def warning(data, sector=None):
    if sector is not None:
        data['sector'] = sector
    logger.warning(
        json.dumps(data, cls=DJLogEncoder)
    )

def debug(data, sector=None):
    if sector is not None:
        data['sector'] = sector
    logger.debug(
        json.dumps(data, cls=DJLogEncoder)
    )

def error(data, sector=None):
    if sector is not None:
        data['sector'] = sector
    logger.debug(
        json.dumps(data, cls=DJLogEncoder)
    )