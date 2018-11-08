"""
Test Module for Main API Methods
"""
import os
from collections import OrderedDict
from datetime import timedelta
from urllib.parse import urljoin

import requests_mock
from django.conf import settings
from django.contrib.gis.geos import Point
from django.test import override_settings
from model_mommy import mommy

from kaznet.apps.main.api import (create_submission, validate_location,
                                  validate_submission_limit,
                                  validate_submission_time, validate_user)
from kaznet.apps.main.common_tags import (INCORRECT_LOCATION,
                                          INVALID_SUBMISSION_TIME,
                                          LACKING_EXPERTISE,
                                          SUBMISSIONS_MORE_THAN_LIMIT)
from kaznet.apps.main.models import Submission, Task
from kaznet.apps.main.serializers import KaznetLocationSerializer
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.api import process_instance
from kaznet.apps.ona.models import Instance
from kaznet.apps.ona.tests.test_api import MOCKED_ONA_FORM_DATA
from kaznet.apps.users.models import UserProfile

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestAPIMethods(MainTestBase):
    """
    Test class for API Methods
    """

    def setUp(self):
        super().setUp()

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
    @requests_mock.Mocker()
    def _create_instance(self, mocked, pending: bool = False):
        """
        Helper method to create an instance with
        valid data
        """
        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/53/form.json'),
            json=MOCKED_ONA_FORM_DATA
        )
        mocked.post(
            urljoin(settings.ONA_BASE_URL, 'api/v1/dataviews'),
            status_code=201
        )
        mommy.make('auth.User', username='dave')
        mommy.make('ona.Project', ona_pk=49)
        form = mommy.make('ona.XForm', ona_pk=25, ona_project_id=49)

        mommy.make('main.Task', target_content_type=self.xform_type,
                   target_content_object=form)

        data = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_geolocation": [
                36.776554,
                -1.294328
            ],
            "_status": "submitted_via_web",
            "_review_status": settings.ONA_SUBMISSION_REVIEW_APPROVED,
            "_review_comments": "This is a review comment",
            "_submitted_by": "dave",
            "_xform_id": 25,
            "_submission_time": "2019-09-01T07:42:07",
            "_version": "vvadCJQ9XjXXSMmFSnKZqK",
            "_attachments": [],
            "_id": 17
        }

        if pending:
            data["_review_status"] = settings.ONA_SUBMISSION_REVIEW_PENDING
            data["_review_comments"] = ""
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

        mommy.make(
            'main.TaskLocation', task=task, location=location,
            start='09:00:00', end='19:00:00',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')

        data = instance.json

        validated_location, status, comment = validate_location(
            data[settings.ONA_GEOLOCATION_FIELD], task)

        self.assertEqual(location, validated_location)
        self.assertEqual(Submission.PENDING, status)
        self.assertEqual("", comment)

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

        mommy.make(
            'main.TaskLocation', task=task, location=mocked_location,
            start='09:00:00', end='19:00:00',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')

        data = instance.json

        invalid_location, status, comment = validate_location(
            data[settings.ONA_GEOLOCATION_FIELD], task)

        self.assertEqual(None, invalid_location)
        self.assertEqual(Submission.REJECTED, status)
        self.assertEqual(INCORRECT_LOCATION, comment)

    def test_validate_user(self):
        """
        Test that validate_user works the way it should
        for valid data
        """
        instance = self._create_instance()
        user = instance.user
        user.userprofile.expertise = UserProfile.ADVANCED

        task = mommy.make(
            'main.Task',
            required_expertise=Task.INTERMEDIATE,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        status, comment = validate_user(task, user)

        self.assertEqual(Submission.PENDING, status)
        self.assertEqual("", comment)

    def test_validate_user_with_invalid_data(self):
        """
        Test that validate user works the way it should for
        invalid data
        """
        instance = self._create_instance()
        user = instance.user
        user.userprofile.expertise = UserProfile.BEGINNER

        task = mommy.make(
            'main.Task',
            required_expertise=Task.INTERMEDIATE,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        status, comment = validate_user(task, user)

        self.assertEqual(Submission.REJECTED, status)
        self.assertEqual(LACKING_EXPERTISE, comment)

    def test_validate_submission_time(self):
        """
        Test that validate_submission_time works the way
        it should for valid data
        """
        instance = self._create_instance()
        data = instance.json
        rrule = 'FREQ=DAILY;INTERVAL=1;UNTIL=20310729T210000Z'

        task = mommy.make(
            'main.Task',
            timing_rule=rrule,
            target_content_type=self.xform_type,
            target_object_id=instance.xform.id)

        data['_submission_time'] = (
            task.start + timedelta(minutes=45)).isoformat()

        status, comment = validate_submission_time(
            task, data['_submission_time'])

        self.assertEqual(Submission.PENDING, status)
        self.assertEqual("", comment)

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

        status, comment = validate_submission_time(
            task, data['_submission_time'])

        self.assertEqual(Submission.REJECTED, status)
        self.assertEqual(INVALID_SUBMISSION_TIME, comment)

    def test_validate_submission_limit(self):
        """
        Test that validate_submission_limit works as it should with valid data
        """
        instance = self._create_instance()
        task = instance.get_task()
        user = instance.user
        task.user_submission_target = 2
        task.rrule = 'FREQ=DAILY;INTERVAL=1;UNTIL=20210729T210000Z'
        task.save()

        userprofile = instance.user.userprofile
        data = instance.json

        userprofile.expertise = '4'
        data['_submission_time'] = "2019-09-01T20:00:00"

        mommy.make('main.Bounty', task=task, amount=4000)

        mocked_location = mommy.make(
            'main.Location', geopoint=Point(36.806852, -1.313721), radius=10)
        mommy.make(
            'main.TaskLocation', task=task, location=mocked_location,
            start='09:00:00', end='19:00:00',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')

        create_submission(instance)

        status, comment = validate_submission_limit(task, user)
        self.assertEqual(Submission.PENDING, status)
        self.assertEqual("", comment)

    def test_validate_submission_limit_with_invalid_data(self):
        """
        Test that validate_submission_limit works as it should with invalid
        data
        """
        instance = self._create_instance()
        task = instance.get_task()
        user = instance.user
        task.user_submission_target = 1
        task.rrule = 'FREQ=DAILY;INTERVAL=1;UNTIL=20210729T210000Z'
        task.save()

        userprofile = instance.user.userprofile
        data = instance.json

        userprofile.expertise = '4'
        data['_submission_time'] = "2019-09-01T20:00:00"

        mommy.make('main.Bounty', task=task, amount=4000)

        mocked_location = mommy.make(
            'main.Location', geopoint=Point(36.806852, -1.313721), radius=10)
        mommy.make(
            'main.TaskLocation', task=task, location=mocked_location,
            start='09:00:00', end='19:00:00',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')

        # create two submissions
        create_submission(instance)
        create_submission(instance)

        status, comment = validate_submission_limit(task, user)
        self.assertEqual(Submission.REJECTED, status)
        self.assertEqual(SUBMISSIONS_MORE_THAN_LIMIT, comment)

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
        data['_submission_time'] = "2019-09-01T20:00:00"

        rrule = 'FREQ=DAILY;INTERVAL=1;UNTIL=20210729T210000Z'

        task = instance.get_task()
        task.timing_rule = rrule
        task.save()

        mocked_bounty = mommy.make('main.Bounty', task=task, amount=4000)

        mocked_location = mommy.make(
            'main.Location', geopoint=Point(36.806852, -1.313721), radius=10)
        mommy.make(
            'main.TaskLocation', task=task, location=mocked_location,
            start='09:00:00', end='19:00:00',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')

        instance.refresh_from_db()

        submission = create_submission(instance)

        self.assertEqual(Submission.APPROVED, submission.status)
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

        instance = self._create_instance(pending=True)
        userprofile = instance.user.userprofile
        data = instance.json

        userprofile.expertise = '1'
        data['_submission_time'] = "2018-07-18T21:00:00"

        rrule = 'FREQ=DAILY;INTERVAL=1;UNTIL=20210729T210000Z'

        task = instance.get_task()
        task.timing_rule = rrule
        task.required_expertise = Task.ADVANCED
        task.save()

        mommy.make('main.Bounty', task=task, amount=4000)

        mocked_location = mommy.make(
            'main.Location', geopoint=Point(36.806852, -1.313721), radius=10)
        mommy.make(
            'main.TaskLocation', task=task, location=mocked_location,
            start='09:00:00', end='19:00:00',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')

        submission = create_submission(instance)

        self.assertEqual(Submission.REJECTED, submission.status)
        self.assertEqual(LACKING_EXPERTISE, submission.comments)

    def test_create_reviewed_submission(self):
        """
        Test that creation of submission based on review status
         - reviewed submissions don't go through time, location validation
         - update location fields for reviewed submissions
         """
        instance = self._create_instance()
        userprofile = instance.user.userprofile
        data = instance.json

        userprofile.expertise = '4'
        data['_submission_time'] = "2019-09-01T20:00:00"

        rrule = 'FREQ=DAILY;INTERVAL=1;UNTIL=20210729T210000Z'

        task = instance.get_task()
        task.timing_rule = rrule
        task.required_expertise = Task.INTERMEDIATE
        task.save()

        mocked_bounty = mommy.make('main.Bounty', task=task, amount=4000)

        mocked_location = mommy.make(
            'main.Location', geopoint=Point(36.806852, -1.313721), radius=10)
        mommy.make(
            'main.TaskLocation', task=task, location=mocked_location,
            start='09:00:00', end='19:00:00',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')

        submission = create_submission(instance)
        self.assertEqual(Submission.APPROVED, submission.status)
        self.assertEqual(mocked_location, submission.location)
        self.assertEqual(mocked_bounty, submission.bounty)
        self.assertEqual(task, submission.task)
        self.assertEqual(instance.user, submission.user)
        self.assertTrue(submission.valid)
