"""
Test for KaznetSubmissionSerializer
"""
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.utils import timezone

import pytz
from model_mommy import mommy

from kaznet.apps.main.models import Submission
from kaznet.apps.main.serializers import (KaznetSubmissionSerializer,
                                          SubmissionExportSerializer)
from kaznet.apps.main.tests.base import MainTestBase

USER = get_user_model()


class SubmissionSerializerBase(MainTestBase):
    """
    Base class for SubmissionSerializer tests
    """

    def _create_submission(self):
        """
        Test that the serializer creates a submission
        """
        self.now = timezone.now()
        mocked_target_object = mommy.make('ona.Instance')
        mocked_task = mommy.make('main.Task', name='Cow Prices')
        mocked_location = mommy.make('main.Location', name='Nairobi')
        mocked_user = mommy.make(
            'auth.User', username='Bob', first_name='Bob', last_name='Kamau')
        mocked_bounty = mommy.make('main.Bounty', task=mocked_task, amount=99)

        data = {
            'task': {
                "type": "Task",
                "id": mocked_task.id
            },
            'location': {
                "type": "Location",
                "id": mocked_location.id
            },
            'submission_time': self.now,
            'user': {
                "type": "User",
                "id": mocked_user.id
            },
            'bounty': {
                "type": "Bounty",
                "id": mocked_bounty.id
            },
            'comments': 'Approved',
            'status': Submission.REJECTED,
            'valid': True,
            'target_content_type': self.instance_type.id,
            'target_id': mocked_target_object.id,
        }

        serializer_instance = KaznetSubmissionSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        submission = serializer_instance.save()

        # the subsmission_time field is going to be converted to isformat
        data['submission_time'] = self.now.astimezone(
            pytz.timezone('Africa/Nairobi')).isoformat()

        # we get OrderedDict(s) so we convert it to a dict for comparison
        # also, the task id gets back as a string
        data['task']['id'] = str(data['task']['id'])
        data['bounty']['id'] = str(data['bounty']['id'])
        data['user']['id'] = str(data['user']['id'])
        data['location']['id'] = str(data['location']['id'])
        instance_dict = serializer_instance.data.copy()
        instance_dict['task'] = dict(instance_dict['task'])
        instance_dict['bounty'] = dict(instance_dict['bounty'])
        instance_dict['location'] = dict(instance_dict['location'])
        instance_dict['user'] = dict(instance_dict['user'])

        self.assertDictContainsSubset(data, instance_dict)

        self.assertEqual(mocked_task, submission.task)
        self.assertEqual(mocked_location, submission.location)
        self.assertEqual(mocked_user, submission.user)
        self.assertEqual(self.now, submission.submission_time)
        self.assertEqual('Approved', submission.comments)
        self.assertEqual(Submission.REJECTED, submission.status)
        self.assertTrue(submission.valid)

        # assert Submission approved property is False when status is REJECTED
        self.assertFalse(submission.approved)

        # set Submission status to APPROVED and test that approved is True
        submission.status = Submission.APPROVED
        self.assertTrue(submission.approved)

        expected_fields = {
            'task',
            'location',
            'submission_time',
            'user',
            'comments',
            'status',
            'valid',
            'approved',
            'bounty',
            'amount',
            'target_content_type',
            'target_id',
            'id',
            'created',
            'modified'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))

        return submission


class TestKaznetSubmissionSerializer(SubmissionSerializerBase):
    """
    Tests for KaznetSubmissionSerializer
    """

    def test_create_submission(self):
        """
        Test that the serializer creates a submission
        """
        self._create_submission()

    def test_validate_bad_data(self):
        """
        Test validate method of SubmissionSerializer works as expected
        for bad data
        """
        now = timezone.now()
        mocked_target_object = mommy.make('ona.Instance')
        mocked_task = mommy.make('main.Task', name='Cow Prices')
        mocked_location = mommy.make('main.Location', name='Nairobi')
        mocked_user = mommy.make(
            'auth.User', username='Bob', first_name='Bob', last_name='Kamau')

        bad_target_id = OrderedDict(
            task=mocked_task.id,
            location=mocked_location.id,
            submission_time=now,
            user=mocked_user.id,
            comments='Approved',
            status=Submission.APPROVED,
            valid=True,
            target_content_type=self.instance_type.id,
            target_id=5487,
        )

        self.assertFalse(
            KaznetSubmissionSerializer(data=bad_target_id).is_valid())

        bad_content_type = OrderedDict(
            task=mocked_task.id,
            location=mocked_location.id,
            submission_time=now,
            user=mocked_user.id,
            comments='Approved',
            status=Submission.APPROVED,
            valid=True,
            target_content_type='foobar',
            target_id=mocked_target_object.id,
        )

        self.assertFalse(
            KaznetSubmissionSerializer(data=bad_content_type).is_valid())


class TestSubmissionExportSerializer(SubmissionSerializerBase):
    """
    Tests for SubmissionExportSerializer
    """

    def test_submission_serializer_output(self):
        """
        """
        submission = self._create_submission()

        userprofile = submission.user.userprofile
        userprofile.phone_number = '+254722000000'
        userprofile.payment_number = '+254722000000'

        serializer_instance = SubmissionExportSerializer(submission)

        expected_fields = {
            'id',
            'user',
            'approved',
            'status',
            'comments',
            'task',
            'location',
            'submission_time',
            'amount',
            'currency',
            'phone_number',
            'payment_number',
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))

        self.assertEqual(submission.id, serializer_instance.data['id'])
        self.assertEqual("Bob Kamau", serializer_instance.data['user'])
        self.assertEqual("Cow Prices", serializer_instance.data['task'])
        self.assertEqual("Nairobi", serializer_instance.data['location'])
        self.assertEqual(
            self.now.astimezone(pytz.timezone('Africa/Nairobi')).isoformat(),
            serializer_instance.data['submission_time'])
        self.assertEqual(
            Submission.APPROVED, serializer_instance.data['status'])
        self.assertEqual('99.00', serializer_instance.data['amount'])
        self.assertEqual('KES', serializer_instance.data['currency'])
        self.assertEqual(
            '+254722000000', serializer_instance.data['phone_number'])
        self.assertEqual(
            '+254722000000', serializer_instance.data['payment_number'])
