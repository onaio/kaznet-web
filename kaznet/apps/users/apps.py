# -*- coding: utf-8 -*-
"""
Apps Module for Users
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Users AppConfig
    """
    name = 'kaznet.apps.users'

    def ready(self):
        # pylint: disable=unused-import
        import kaznet.apps.users.signals  # noqa
