"""
Module for the Location model(s)
"""
from django.utils.translation import ugettext as _
from django.db import models

from tasking.models import BaseLocation


class Location(BaseLocation):
    """
    Location model class
    """

    location_type = models.ForeignKey(
        'main.LocationType',
        verbose_name=_('Location Type'),
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        help_text=_('This represents the Location Type')
    )

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the Location model
        """
        abstract = False
        ordering = ['country', 'name', 'id']
        app_label = 'main'

    # pylint: disable=no-else-return
    def __str__(self):
        """
        String representation of a Location object

        e.g. Kenya - Nairobi
        """
        if self.country.name != '':
            return _(f"{self.country.name} - {self.name}")
        else:
            return _(f"{self.name}")

    def get_parent_name(self):
        """
        Custom method to get parent name
        """
        try:
            return self.parent.name
        except AttributeError:
            return 'None'

    def get_location_type_name(self):
        """
        Custom method to get location_type name
        """
        try:
            return self.location_type.name
        except AttributeError:
            return 'None'

    @property
    def parent_name(self):
        """
        Returns the parent locations name
        """
        return self.get_parent_name()

    @property
    def location_type_name(self):
        """
        Returns the location_types name
        """
        return self.get_location_type_name()
