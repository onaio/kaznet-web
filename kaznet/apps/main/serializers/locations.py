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

from kaznet.apps.main.common_tags import SAME_PARENT
from kaznet.apps.main.models import Location
from kaznet.apps.main.serializers.base import validate_parent_field


# pylint: disable=too-many-ancestors
class KaznetLocationSerializer(serializers.ModelSerializer):
    """
    KaznetLocationSerializer serializer class
    """
    country = SerializableCountryField(
        allow_blank=True, required=False, choices=Countries())

    shapefile = ShapeFileField(required=False)
    geopoint = GeopointField(required=False)

    # pylint: disable=too-few-public-methods
    class Meta:
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
            'modified',
            'has_submissions',
        ]

    def validate_parent(self, value):
        """
        Validate location parent field
        """
        if self.instance is not None and not validate_parent_field(
                self.instance, value):
            # locations cannot be their own parents
            raise serializers.ValidationError(SAME_PARENT)
        return value

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
        if shapefile is not None:
            if radius is not None:
                raise serializers.ValidationError(
                    {'radius': GEODETAILS_ONLY}
                )
            if geopoint is not None:
                raise serializers.ValidationError(
                    {'geopoint': GEODETAILS_ONLY}
                )

        return super().validate(attrs)

    def update(self, instance, validated_data):
        """
        Custom method to perform Location Update
        """

        geopoint = validated_data.get('geopoint')
        radius = validated_data.get('radius')
        shapefile = validated_data.get('shapefile')

        # remove shapefile if post data has geopoint and radius
        if geopoint is not None and radius is not None:
            instance.radius = radius
            instance.geopoint = geopoint
            if instance.shapefile:
                instance.shapefile = None

        # remove geopoint and radius if post data has shapefile
        elif shapefile is not None:
            instance.shapefile = shapefile
            if instance.geopoint or instance.radius:
                instance.radius = None
                instance.geopoint = None

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.save()
        return super().update(instance, validated_data)
