"""
Module for the LocationType model
"""
from tasking.models import BaseLocationType


class LocationType(BaseLocationType):
    """
    LocationType model class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for LocationType
        """
        abstract = False
        ordering = ['name', 'id']
        app_label = 'main'

    def __str__(self):
        """
        String representation for LocationType Model
        e.g Harbor
        """

        return self.name
