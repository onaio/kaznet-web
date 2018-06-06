"""
Main Location serializer module
"""
from tasking.serializers import LocationSerializer

from kaznet.apps.main.models import Location


class KaznetLocationSerializer(LocationSerializer):
    """
    Main Location Serializer
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for KaznetLocationSerializer
        """
        model = Location
        fields = [
            'id',
            'name',
            'country',
            'description',
            'geopoint',
            'radius',
            'shapefile',
            'parent',
            'created',
            'modified'
        ]
