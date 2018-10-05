"""
Tests for KaznetLocationSerializer
"""

import os
from collections import OrderedDict

from django.test import TestCase

from model_mommy import mommy
from rest_framework.exceptions import ValidationError
from rest_framework_gis.fields import GeoJsonDict
from tasking.common_tags import (GEODETAILS_ONLY, GEOPOINT_MISSING,
                                 RADIUS_MISSING)

from kaznet.apps.main.serializers import KaznetLocationSerializer
from kaznet.apps.main.serializers.base import validate_parent_field

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestLocationSerializer(TestCase):
    """
    Test the LocationSerializer
    """

    def test_location_create(self):
        """
        Test that the serializer can create Location Objects
        """
        data = {
            'name': 'Nairobi',
            'country': 'KE',
            }
        serializer_instance = KaznetLocationSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        location = serializer_instance.save()

        self.assertEqual('Nairobi', location.name)
        self.assertEqual('KE', location.country)
        self.assertEqual('Kenya - Nairobi', str(location))

        expected_fields = [
            'id',
            'modified',
            'parent',
            'radius',
            'country',
            'description',
            'parent_name',
            'location_type_name',
            'location_type',
            'created',
            'geopoint',
            'name',
            'shapefile',
            'has_submissions'
        ]
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data)))

    def test_location_parent_link(self):
        """
        Test the parent link between locations
        """
        mocked_location_parent = mommy.make('main.Location', name='Nairobi')
        data = {
            'name': 'Nairobi',
            'parent': {
                "type": "Location",
                "id": mocked_location_parent.id
            }
        }

        serializer_instance = KaznetLocationSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        location = serializer_instance.save()

        self.assertEqual(mocked_location_parent, location.parent)

    def test_validate_bad_data(self):
        """
        Test validate method of LocationSerializer works as expected
        for bad data
        """
        mocked_location_with_shapefile = mommy.make(
            'main.Location',
            name='Nairobi',
            _fill_optional=['shapefile'])
        missing_radius = OrderedDict(
            name='Nairobi',
            geopoint='30,10')
        missing_geopoint = OrderedDict(
            name='Montreal',
            radius=45.678)
        shapefile_radius = OrderedDict(
            name='Arusha',
            radius=56.6789,
            geopoint='30,10',
            shapefile=mocked_location_with_shapefile.shapefile)

        with self.assertRaises(ValidationError) as missing_radius_cm:
            KaznetLocationSerializer().validate(missing_radius)

        radius_error_detail = missing_radius_cm.exception.detail['radius']
        self.assertEqual(RADIUS_MISSING, str(radius_error_detail))

        with self.assertRaises(ValidationError) as missing_geopoint_cm:
            KaznetLocationSerializer().validate(missing_geopoint)

        geopnt_error_detail = missing_geopoint_cm.exception.detail['geopoint']
        self.assertEqual(GEOPOINT_MISSING, str(geopnt_error_detail))

        with self.assertRaises(ValidationError) as shapefile_radius_cm:
            KaznetLocationSerializer().validate(shapefile_radius)

        shape_error_detail = shapefile_radius_cm.exception.detail['shapefile']
        self.assertEqual(GEODETAILS_ONLY, str(shape_error_detail))

    def test_location_serializer_validate_shapefile(self):
        """
        Test validate method of TaskSerializer works as expected for shapefile
        """
        mocked_location_with_shapefile = mommy.make(
            'main.Location',
            name='Nairobi',
            _fill_optional=['shapefile'])
        data = OrderedDict(
            name='Montreal',
            shapefile=mocked_location_with_shapefile.shapefile)

        validated_data = KaznetLocationSerializer().validate(data)
        self.assertDictEqual(dict(data), dict(validated_data))

    def test_location_serializer_validate_geodetails(self):
        """
        Test validate method of TaskSerializer works as expecter for
        geopoint and radius
        """
        data = OrderedDict(
            name='Spain',
            geopoint='30,10',
            radius=45.986,
            )
        validated_data = KaznetLocationSerializer().validate(data)
        self.assertDictEqual(dict(data), dict(validated_data))

    def test_geopoint_field_output(self):
        """
        Test the geopoint field outputs valid GEOJSON
        """
        data = OrderedDict(
            name='Spain',
            geopoint='30,10',
            radius=45.986,
            )
        serializer_instance = KaznetLocationSerializer(data=data)

        self.assertTrue(serializer_instance.is_valid())
        self.assertEqual(
            type(serializer_instance.data['geopoint']), GeoJsonDict)

    def test_shapefile_field_output(self):
        """
        Test the shapefile field outputs valid GEOJSON
        """
        path = os.path.join(
            BASE_DIR, 'fixtures', 'test_shapefile.zip')

        with open(path, 'r+b') as shapefile:
            data = OrderedDict(
                name='Nairobi',
                country='KE',
                shapefile=shapefile
            )
            serializer_instance = KaznetLocationSerializer(data=data)

            self.assertTrue(serializer_instance.is_valid())
            self.assertEqual(
                type(serializer_instance.data['shapefile']), GeoJsonDict)

    def test_location_update(self):
        """
        Test update method:
        - Keep either the shapefile or radius and geopoint
        """
        mocked_location = mommy.make('main.Location', name='Nairobi')
        data = OrderedDict(
            name='Nairobi',
            geopoint='30,10',
            radius=45.986,
        )
        create_serializer_instance = KaznetLocationSerializer(
            instance=mocked_location, data=data)
        self.assertTrue(create_serializer_instance.is_valid())
        create_serializer_instance.save()
        self.assertEqual(
            type(create_serializer_instance.data['geopoint']), GeoJsonDict)
        self.assertEqual(
            float(create_serializer_instance.data['radius']), data['radius'])

        path = os.path.join(
            BASE_DIR, 'fixtures', 'test_shapefile.zip')

        # removes geopoint and radius data given shapefile
        with open(path, 'r+b') as shapefile:
            data = OrderedDict(
                name='Nairobi',
                shapefile=shapefile
            )
            update_serializer_instance = KaznetLocationSerializer(
                instance=mocked_location, data=data)
            self.assertTrue(update_serializer_instance.is_valid())
            update_serializer_instance.save()
            self.assertEqual(update_serializer_instance.data['geopoint'], None)
            self.assertEqual(update_serializer_instance.data['radius'], None)
            self.assertEqual(
                type(update_serializer_instance.data['shapefile']),
                GeoJsonDict)

    def test_validate_parent(self):
        """
        Test parent location validation
        """
        mocked_location = mommy.make('main.Location', name='Nairobi')
        # Invalid, location cannot be it's own parent
        self.assertFalse(
            validate_parent_field(mocked_location, mocked_location))

        # A different location can be a parent
        mocked_parent_location = mommy.make('main.Location', name='Nairobi')
        self.assertTrue(
            validate_parent_field(mocked_location, mocked_parent_location))
