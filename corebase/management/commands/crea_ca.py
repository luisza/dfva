from django.core.management.base import BaseCommand
from corebase.ca_management.simpleCA.build_ca import build_ca


class Command(BaseCommand):
    help = 'Construye una Autoridad Certificadora'

    def handle(self, *args, **options):
        build_ca()
