"""
Test Module for Main API Methods
"""
import os
from collections import OrderedDict

from django.contrib.gis.geos import Point

from model_mommy import mommy

from kaznet.apps.main.api import (validate_location, validate_submission_time,
                                  validate_user)
from kaznet.apps.main.common_tags import (INCORRECT_LOCATION,
                                          INVALID_SUBMISSION_TIME,
                                          LACKING_EXPERTISE)
from kaznet.apps.main.models import Task
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

    def test_validate_location(self):
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

    def test_validate_user(self):
        """
        Test that validate_user works the way it should
        for valid data
        """
        instance = self._create_instance()
        user = instance.user
        data = instance.json
        user.userprofile.expertise = '4'

        task = mommy.make(
            'main.Task',
            required_expertise=Task.BEGINNER,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        validated_data = validate_user(data, task, user)

        self.assertEqual('d', validated_data['status'])

    def test_validate_user_with_invalid_data(self):
        """
        Test that validate user works the way it should for
        invalid data
        """
        instance = self._create_instance()
        user = instance.user
        data = instance.json
        user.userprofile.expertise = '1'

        task = mommy.make(
            'main.Task',
            required_expertise=Task.INTERMEDIATE,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        validated_data = validate_user(data, task, user)

        self.assertEqual('b', validated_data['status'])
        self.assertEqual(LACKING_EXPERTISE, validated_data['comments'])

    def test_validate_submission_time(self):
        """
        Test that validate_submission_time works the way
        it should for valid data
        """
        instance = self._create_instance()
        data = instance.json

        data['_submission_time'] = "2018-06-18T07:42:07"

        task = mommy.make(
            'main.Task',
            timing_rule='FREQ=DAILY;INTERVAL=1;UNTIL=20180618T210000Z',
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        validated_data = validate_submission_time(task, data)

        self.assertEqual('d', validated_data['status'])

    def test_validate_submission_time_with_invalid_data(self):
        """
        Test that validate_submission_time works the way it should
        for invalid data
        """
        instance = self._create_instance()
        data = instance.json

        data['_submission_time'] = "2018-06-18T22:42:07"

        task = mommy.make(
            'main.Task',
            timing_rule='FREQ=DAILY;INTERVAL=1;UNTIL=20180618T210000Z',
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        validated_data = validate_submission_time(task, data)

        self.assertEqual('b', validated_data['status'])
        self.assertEqual(INVALID_SUBMISSION_TIME, validated_data['comments'])

    def test_create_submission(self):
        """
        Test that create_submission works the way it should
        for valid data
        """

        # Test it creates a Submission Object If Data is Valid

        # Test it calls validate_user

        # Test it calls validate_location if validate_user passes

        # Test it calls validate_submission_time if validate_user
        # and validate_location passes
        pass

    def test_create_submission_with_invalid_data(self):
        """
        Test that create_submission works the way it should for invalid
        data
        """

        # Test it creates a Submission Object with Rejected as status if
        # Data Fails a validation
        pass
