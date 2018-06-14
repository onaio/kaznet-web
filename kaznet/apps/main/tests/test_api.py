"""
Test Module for Main API Methods
"""
import os
from collections import OrderedDict

from django.contrib.gis.geos import Point

from model_mommy import mommy

from kaznet.apps.main.api import validate_location
from kaznet.apps.main.common_tags import INCORRECT_LOCATION
from kaznet.apps.main.serializers import KaznetLocationSerializer
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.api import process_instance
from kaznet.apps.ona.models import Instance

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestAPIMethods(MainTestBase):
    """
    Test class for API Methods
    """

    def _create_instance(self):
        """
        Helper method to create an instance with
        valid data
        """
        mommy.make('auth.User', username='dave')
        mommy.make('ona.Project', ona_pk=49)
        form = mommy.make('ona.XForm', ona_pk=25, project_id=49)

        data = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_geolocation": [
                36.776554,
                -1.294328
            ],
            "_status": "submitted_via_web",
            "_submitted_by": "dave",
            "_xform_id": 25,
            "_submission_time": "2018-05-30T07:42:07",
            "_version": "vvadCJQ9XjXXSMmFSnKZqK",
            "_attachments": [],
            "_id": 17
        }
        process_instance(data, xform=form)

        return Instance.objects.get(ona_pk=17)

    def test_validate_location_with_valid_data(self):
        """
        Test that validate_location works
        the way it should for valid data
        """
        instance = self._create_instance()
        task = mommy.make(
            'main.Task',
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        path = os.path.join(
            BASE_DIR, 'tests', 'fixtures', 'test_shapefile.zip')

        with open(path, 'r+b') as shapefile:
            data = OrderedDict(
                name='Nairobi',
                country='KE',
                shapefile=shapefile
            )
            serializer_instance = KaznetLocationSerializer(data=data)
            serializer_instance.is_valid()

            location = serializer_instance.save()

        task.locations.add(location)

        data = instance.json

        validated_data = validate_location(data, task)

        self.assertEqual(location, validated_data['location'])
        self.assertEqual('d', validated_data['status'])

    def test_validate_location_with_invalid_data(self):
        """
        Test that validate_location works the way
        it should for invalid data
        """
        instance = self._create_instance()
        task = mommy.make(
            'main.Task',
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)
        mocked_location = mommy.make(
            'main.Location', geopoint=Point(36.806852, -1.313721), radius=1)
        task.locations.add(mocked_location)

        data = instance.json

        validated_data = validate_location(
            data, task)

        self.assertEqual('b', validated_data['status'])
        self.assertEqual(
            INCORRECT_LOCATION, validated_data['comments'])
