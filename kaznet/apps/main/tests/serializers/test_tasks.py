"""
Test  module for main Task serializers
"""

from collections import OrderedDict
from datetime import timedelta

from django.utils import timezone

from dateutil.rrule import rrulestr
from django_prices.models import Money
from model_mommy import mommy
from tasking.utils import get_rrule_end, get_rrule_start

from kaznet.apps.main.models import Bounty
from kaznet.apps.main.serializers import KaznetTaskSerializer
from kaznet.apps.main.tests.base import MainTestBase


class TestKaznetTaskSerializer(MainTestBase):
    """
    Test the KaznetTaskSerializer
    """

    def test_validate_bad_data(self):
        """
        Test validate method of KaznetTaskSerializer works as expected
        for bad data
        """
        mocked_target_object = mommy.make('ona.XForm')

        bad_target_id = OrderedDict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type=self.xform_type.id,
            target_id=1337
        )

        self.assertFalse(KaznetTaskSerializer(data=bad_target_id).is_valid())

        bad_content_type = OrderedDict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type='foobar',
            target_id=mocked_target_object.id,
        )

        self.assertFalse(
            KaznetTaskSerializer(data=bad_content_type).is_valid())

    def test_create_task(self):
        """
        Test that the serializer can create Task objects
        """
        mocked_target_object = mommy.make('ona.XForm')

        rule1 = mommy.make('main.SegmentRule')
        rule2 = mommy.make('main.SegmentRule')

        rrule = 'DTSTART:20180521T210000Z RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'total_submission_target': 10,
            'timing_rule': rrule,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'estimated_time': 'P4DT1H15M20S',
        }

        data_with_segment_rules = data.copy()
        data_with_segment_rules['segment_rules'] = [rule1.id, rule2.id]

        serializer_instance = KaznetTaskSerializer(
            data=data_with_segment_rules)
        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        # the start and end fields are going to be from the timing rule
        start = get_rrule_start(rrulestr(rrule))
        end = get_rrule_end(rrulestr(rrule))

        # Change estimated time to DD HH:MM:SS format since Serializer
        # Changes it to such
        data['estimated_time'] = '4 01:15:20'

        # the order of segment_rules may have changed so a dict comparison
        # may fail, we use `data` that does not include segment rules
        self.assertDictContainsSubset(data, serializer_instance.data)

        # we test that we do have our segment rules
        self.assertEqual(set([rule1.id, rule2.id]),
                         set(serializer_instance.data['segment_rules']))

        # we test that submissions are equal to 0
        self.assertEqual(serializer_instance.data['submission_count'], 0)
        self.assertEqual(task.submissions, 0)

        # we test that rejectedsubmissions are equal to 0
        self.assertEqual(
            serializer_instance.data['rejected_submissions_count'], 0)
        self.assertEqual(task.rejected_submissions_count, 0)

        # we test that pending submissions are equal to 0
        self.assertEqual(
            serializer_instance.data['pending_submissions_count'], 0)
        self.assertEqual(task.pending_submissions_count, 0)

        # we test that approved submissions are equal to 0
        self.assertEqual(
            serializer_instance.data['approved_submissions_count'], 0)
        self.assertEqual(task.approved_submissions_count, 0)

        # we test that approved submissions are equal to 0
        self.assertEqual(
            serializer_instance.data['total_bounty_payout'], Money(0, 'KES'))
        self.assertEqual(task.total_bounty_payout, Money(0, 'KES'))

        # Add a submission to task and assert it changes.
        mocked_submission = mommy.make('main.Submission', task=task)
        self.assertTrue(mocked_submission.task, task)
        self.assertEqual(task.submissions, 1)

        self.assertEqual('Cow price', task.name)
        self.assertEqual('Some description', task.description)
        self.assertEqual(start, task.start)
        self.assertEqual(end, task.end)
        self.assertEqual(10, task.total_submission_target)

        # assert that the ISO 8601 String was converted to accurately
        self.assertEqual(task.estimated_time, timedelta(4, 4520))

        # test that the segment rules for the task are as we expect
        self.assertEqual(rule1, task.segment_rules.get(id=rule1.id))
        self.assertEqual(rule2, task.segment_rules.get(id=rule2.id))

        # test no bounty was created since amount wasn't passed
        # pylint: disable=no-member
        self.assertEqual(Bounty.objects.all().count(), 0)

        expected_fields = [
            'id',
            'created',
            'modified',
            'name',
            'parent',
            'description',
            'approved_submissions_count',
            'pending_submissions_count',
            'rejected_submissions_count',
            'total_bounty_payout',
            'bounty',
            'start',
            'client',
            'end',
            'timing_rule',
            'estimated_time',
            'total_submission_target',
            'user_submission_target',
            'status',
            'submission_count',
            'target_content_type',
            'target_id',
            'segment_rules',
            'locations',
        ]
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))

    def test_create_task_with_bounty(self):
        """
        Test that a bounty is created if Task is passed into
        KaznetTaskSerializer
        """
        mocked_target_object = mommy.make('ona.XForm')

        rrule = 'DTSTART:20180521T210000Z RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'

        initial_data = {
            'name': 'Cow price',
            'description': 'Some description',
            'total_submission_target': 10,
            'timing_rule': rrule,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'estimated_time': 'P4DT1H15M20S',
            'amount': '5400'
        }

        serializer_instance = KaznetTaskSerializer(
            data=initial_data)
        self.assertTrue(serializer_instance.is_valid())

        # No Bounty In System Yet
        # pylint: disable=no-member
        self.assertEqual(Bounty.objects.all().count(), 0)

        task = serializer_instance.save()

        # Bounty should have been created since amount is Present
        self.assertEqual(Bounty.objects.all().count(), 1)

        bounty = Bounty.objects.get(task=task)
        self.assertEqual(task.bounty, bounty)
        self.assertEqual(task, bounty.task)

        updated_data = {
            'name': 'Spaceship Price',
            'description': 'To the moon and back',
            'timing_rule': rrule,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'amount': '10000000'
        }

        # If amount changes in Task update create a new Bounty
        serializer_instance = KaznetTaskSerializer(
            instance=task, data=updated_data)
        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        # Retrieve Created Bounty
        bounty2 = Bounty.objects.get(amount=Money('10000000.00', 'KES'))

        self.assertEqual(bounty2.task, task)
        self.assertEqual(task.bounty, bounty2)
        # Keeps track of previous bounties
        self.assertEqual(bounty.task, task)
        self.assertEqual(Bounty.objects.all().count(), 2)

        # Test doesn't create a new Bounty if Amount hasnt changed

        updated_data = {
            'name': 'Space Price',
            'description': 'To the Infinity',
            'timing_rule': rrule,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'amount': '10000000'
        }

        # If amount changes in Task update create a new Bounty
        serializer_instance = KaznetTaskSerializer(
            instance=task, data=updated_data)
        self.assertTrue(serializer_instance.is_valid())

        # No new Bounty Created
        self.assertEqual(Bounty.objects.all().count(), 2)

    def test_validate_timing_rule(self):
        """
        Test that the serializer timing_rule validation works
        """
        mocked_target_object = mommy.make('ona.XForm')

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'start': timezone.now(),
            'total_submission_target': 10,
            'timing_rule': 'inva;lid',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
        }

        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())

    def test_location_link(self):
        """
        Test the connection of Task and Location
        """
        location = mommy.make('main.location', name='Nairobi', country='KE')
        mocked_target_object = mommy.make('ona.XForm')

        now = timezone.now()

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
        }

        data_with_location = data.copy()
        data_with_location['locations'] = [location.id]

        serializer_instance = KaznetTaskSerializer(data=data_with_location)

        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        self.assertEqual(location, task.locations.get(id=location.id))

    def test_task_parent_link(self):
        """
        Test the connection between a parent and child task
        """
        mocked_parent_task = mommy.make('main.Task', name='Cow Price')
        mocked_target_object = mommy.make('ona.XForm')
        now = timezone.now()

        data = {
            'name': 'Milk Production',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'parent': mocked_parent_task.id
        }

        serializer_instance = KaznetTaskSerializer(data=data)

        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        self.assertEqual(mocked_parent_task, task.parent)

    def test_task_client_link(self):
        """
        Test the connection between a client and task
        """
        mocked_client = mommy.make('main.Client', name='Knights Order')
        mocked_target_object = mommy.make('ona.XForm')
        now = timezone.now()

        data = {
            'name': 'Milk Production',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'client': mocked_client.id
        }

        serializer_instance = KaznetTaskSerializer(data=data)

        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        self.assertEqual(mocked_client, task.client)
