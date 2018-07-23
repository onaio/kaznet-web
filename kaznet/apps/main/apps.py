"""
Apps module for the main kaznet app
"""
from django.apps import AppConfig


class MainConfig(AppConfig):
    """
    Kaznet App Config Class
    """
    name = 'kaznet.apps.main'

    def ready(self):
        # pylint: disable=unused-variable
        import kaznet.apps.main.signals  # noqa
        import kaznet.apps.ona.signals  # noqa
