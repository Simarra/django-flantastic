from django.apps import AppConfig


class FlantasticConfig(AppConfig):
    name = 'flantastic'
    verbose_name = 'flantastic'

    def ready(self):
        import flantastic.signals # noqa
