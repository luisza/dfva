from django.apps import AppConfig


class InstitutionConfig(AppConfig):
    name = 'institution'

    def ready(self):
        import institution.signals  # noqa
