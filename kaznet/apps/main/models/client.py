"""
Module for the Client model
"""
from django.db import models
from django.utils.translation import ugettext as _

from tasking.models.base import TimeStampedModel


class Client(TimeStampedModel):
    """
    Client model class
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('Name of the client.'))

    def __str__(self):
        return self.name
