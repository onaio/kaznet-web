"""
"""

from tasking.models.base import BaseLocation


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

    # pylint: disable=no-else-return
    def __str__(self):
        """
        String representation of a Location object

        e.g. Kenya - Nairobi
        """
        if self.country.name != '':
            return "{country} - {name}".format(
                country=self.country.name,
                name=self.name)
        else:
            return "{name}".format(
                name=self.name)
