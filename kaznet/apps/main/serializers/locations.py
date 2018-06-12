"""
Main Location serializer module
"""
from rest_framework_json_api import serializers
from tasking.serializers import LocationSerializer

from kaznet.apps.main.models import Location


class KaznetLocationSerializer(
        serializers.ModelSerializer, LocationSerializer):
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
