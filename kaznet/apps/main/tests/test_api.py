"""
Test Module for Main API Methods
"""
import os
from collections import OrderedDict

from django.conf import settings
from django.contrib.gis.geos import Point

from model_mommy import mommy

from kaznet.apps.main.api import (create_submission, validate_location,
                                  validate_submission_time, validate_user)
from kaznet.apps.main.common_tags import (INCORRECT_LOCATION,
                                          INVALID_SUBMISSION_TIME,
                                          LACKING_EXPERTISE)
from kaznet.apps.main.models import Submission, Task
from kaznet.apps.main.serializers import KaznetLocationSerializer
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.api import process_instance
from kaznet.apps.ona.models import Instance
from kaznet.apps.users.models import UserProfile

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
        self.assertEqual(
            Submission.PENDING, validated_data[settings.ONA_STATUS_FIELD])

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

        self.assertEqual(Submission.REJECTED, validated_data['status'])
        self.assertEqual(
            INCORRECT_LOCATION, validated_data[settings.ONA_COMMENTS_FIELD])

    def test_validate_user(self):
        """
        Test that validate_user works the way it should
        for valid data
        """
        instance = self._create_instance()
        user = instance.user
        data = instance.json
        user.userprofile.expertise = UserProfile.ADVANCED

        task = mommy.make(
            'main.Task',
            required_expertise=Task.INTERMEDIATE,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        validated_data = validate_user(data, task, user)

        self.assertEqual(
            Submission.PENDING, validated_data[settings.ONA_STATUS_FIELD])

    def test_validate_user_with_invalid_data(self):
        """
        Test that validate user works the way it should for
        invalid data
        """
        instance = self._create_instance()
        user = instance.user
        data = instance.json
        user.userprofile.expertise = UserProfile.BEGINNER

        task = mommy.make(
            'main.Task',
            required_expertise=Task.INTERMEDIATE,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        validated_data = validate_user(data, task, user)

        self.assertEqual(
            Submission.REJECTED, validated_data[settings.ONA_STATUS_FIELD])
        self.assertEqual(
            LACKING_EXPERTISE, validated_data[settings.ONA_COMMENTS_FIELD])

    def test_validate_submission_time(self):
        """
        Test that validate_submission_time works the way
        it should for valid data
        """
        instance = self._create_instance()
        data = instance.json

        data['_submission_time'] = "2018-09-01T20:00:00"
        rrule = 'FREQ=DAILY;INTERVAL=1;UNTIL=20210729T210000Z'

        task = mommy.make(
            'main.Task',
            timing_rule=rrule,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        validated_data = validate_submission_time(task, data)

        self.assertEqual(
            Submission.PENDING, validated_data[settings.ONA_STATUS_FIELD])

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

        self.assertEqual(
            Submission.REJECTED, validated_data[settings.ONA_STATUS_FIELD])
        self.assertEqual(
            INVALID_SUBMISSION_TIME,
            validated_data[settings.ONA_COMMENTS_FIELD])

    def test_create_submission(self):
        """
        Test that create_submission works the way it should
        for valid data
        """

        # Test it creates a Submission Object If Data is Valid
        instance = self._create_instance()
        userprofile = instance.user.userprofile
        data = instance.json

        userprofile.expertise = '4'
        data['_submission_time'] = "2018-09-01T20:00:00"

        rrule = 'FREQ=DAILY;INTERVAL=1;UNTIL=20210729T210000Z'

        task = mommy.make(
            'main.Task',
            timing_rule=rrule,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        mocked_bounty = mommy.make('main.Bounty', task=task, amount=4000)

        mocked_location = mommy.make(
            'main.Location', geopoint=Point(36.806852, -1.313721), radius=10)
        task.locations.add(mocked_location)

        submission = create_submission(instance)

        self.assertEqual(Submission.PENDING, submission.status)
        self.assertEqual(mocked_location, submission.location)
        self.assertEqual(mocked_bounty, submission.bounty)
        self.assertEqual(task, submission.task)
        self.assertEqual(instance.user, submission.user)
        self.assertTrue(submission.valid)

    def test_create_submission_with_invalid_data(self):
        """
        Test that create_submission works the way it should for invalid
        data
        """

        # Test it creates a Submission Object with Rejected as status if
        # Data Fails a validation

        instance = self._create_instance()
        userprofile = instance.user.userprofile
        data = instance.json

        userprofile.expertise = UserProfile.BEGINNER
        data['_submission_time'] = "2018-07-18T21:00:00"

        task = mommy.make(
            'main.Task',
            timing_rule='FREQ=DAILY;INTERVAL=1;UNTIL=20180618T210000Z',
            required_expertise=Task.ADVANCED,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        mommy.make('main.Bounty', task=task, amount=4000)

        mocked_location = mommy.make(
            'main.Location', geopoint=Point(36.806852, -1.313721), radius=10)
        task.locations.add(mocked_location)

        submission = create_submission(instance)

        self.assertEqual(Submission.REJECTED, submission.status)
        self.assertEqual(LACKING_EXPERTISE, submission.comments)
