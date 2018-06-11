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

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for Client Model
        """
        ordering = ['id', 'name']
        app_label = 'main'
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return self.name
