"""
Module for the Location model(s)
"""
from django.utils.translation import ugettext as _

from tasking.models import BaseLocation


class Location(BaseLocation):
    """
    Location model class
    """
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

    @property
    def parent_name(self):
        """
        Returns the parent locations name
        """
        return self.get_parent_name()
