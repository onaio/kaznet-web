"""
LocationType serializer
"""
from rest_framework import serializers

from kaznet.apps.main.models import LocationType


class KaznetLocationTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for LocationType
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for LocationTypeSerializer
        """
        model = LocationType
        fields = [
            'id',
            'created',
            'name',
            'modified'
        ]
