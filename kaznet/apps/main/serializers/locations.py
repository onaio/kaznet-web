"""
Main Location serializer module
"""
from django_countries import Countries
from rest_framework_json_api import serializers
from tasking.common_tags import (GEODETAILS_ONLY, GEOPOINT_MISSING,
                                 RADIUS_MISSING)
from tasking.serializers.location import (GeopointField,
                                          SerializableCountryField,
                                          ShapeFileField)

from kaznet.apps.main.models import Location


# pylint: disable=too-many-ancestors
class KaznetLocationSerializer(serializers.ModelSerializer):
    """
    KaznetLocationSerializer serializer class
    """
    country = SerializableCountryField(
        allow_blank=True, required=False, choices=Countries())

    shapefile = ShapeFileField(required=False)
    geopoint = GeopointField(required=False)

    def validate(self, attrs):
        """
        Custom Validation for KaznetLocationSerializer
        """
        geopoint = attrs.get('geopoint')
        radius = attrs.get('radius')
        shapefile = attrs.get('shapefile')

        if geopoint is not None:
            if shapefile is not None:
                raise serializers.ValidationError(
                    {'shapefile': GEODETAILS_ONLY}
                )
            if radius is None:
                raise serializers.ValidationError(
                    {'radius': RADIUS_MISSING}
                )
        if radius is not None:
            if shapefile is not None:
                raise serializers.ValidationError(
                    {'shapefile': GEODETAILS_ONLY}
                )
            if geopoint is None:
                raise serializers.ValidationError(
                    {'geopoint': GEOPOINT_MISSING}
                )

        return super().validate(attrs)

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
            'parent_name',
            'location_type',
            'location_type_name',
            'description',
            'geopoint',
            'radius',
            'shapefile',
            'parent',
            'created',
            'modified'
        ]
