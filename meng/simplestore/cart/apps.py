from django import apps


class AppConfig(apps.AppConfig):
    name = 'simplestore.cart'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals