"""
Test  module for main Task serializers
"""

from collections import OrderedDict
from datetime import timedelta
from unittest.mock import patch

from dateutil.rrule import rrulestr
from django.utils import timezone
from django_prices.models import Money
from model_mommy import mommy
from tasking.utils import get_rrule_end, get_rrule_start

from kaznet.apps.main.common_tags import PAST_END_DATE
from kaznet.apps.main.models import Bounty, Task
from kaznet.apps.main.serializers import KaznetTaskSerializer
from kaznet.apps.main.tests.base import MainTestBase


class TestKaznetTaskSerializer(MainTestBase):
    """
    Test the KaznetTaskSerializer
    """

    def setUp(self):
        super().setUp()

    def test_validate_bad_data(self):
        """
        Test validate method of KaznetTaskSerializer works as expected
        for bad data
        """
        mocked_target_object = mommy.make('ona.XForm')

        bad_target_id = OrderedDict(
            type="Task",
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
            type="Task",
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
        mocked_target_object = mommy.make(
            'ona.XForm',
            title='Coconut',
            id_string='coconut828',
            version='v828',
            json=dict(
                owner="mosh",
                owner_url="http://example.com/mosh"
            ),
        )

        rule1 = mommy.make('main.SegmentRule')
        rule2 = mommy.make('main.SegmentRule')

        rrule = 'DTSTART:20180521T210000Z RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'

        data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'total_submission_target': 10,
            'timing_rule': rrule,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'estimated_time': 'P4DT1H15M20S',
        }

        data_with_segment_rules = data.copy()
        segment_rules = [
            {
                "type": "SegmentRule",
                "id": rule1.id
            },
            {
                "type": "SegmentRule",
                "id": rule2.id
            }
        ]
        data_with_segment_rules['segment_rules'] = segment_rules

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

        # 'type' is not returns
        data.pop('type')

        # the order of segment_rules may have changed so a dict comparison
        # may fail, we use `data` that does not include segment rules
        self.assertDictContainsSubset(data, serializer_instance.data)

        # we test that we do have our segment rules
        self.assertEqual(2, len(serializer_instance.data['segment_rules']))

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

        # we test that total_bounty_payout is 0
        self.assertEqual(
            serializer_instance.data['total_bounty_payout'], '0 KES')
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

        # check that you get XForm stuff
        self.assertEqual(
            serializer_instance.data['xform_title'],
            mocked_target_object.title)
        self.assertEqual(
            serializer_instance.data['xform_id_string'],
            mocked_target_object.id_string)
        self.assertEqual(
            serializer_instance.data['xform_version'],
            mocked_target_object.version)
        self.assertEqual(
            serializer_instance.data['xform_owner'],
            mocked_target_object.json.get('owner'))
        self.assertEqual(
            serializer_instance.data['xform_owner_url'],
            mocked_target_object.json.get('owner_url'))

        # test no bounty was created since amount wasn't passed
        # pylint: disable=no-member
        self.assertEqual(Bounty.objects.all().count(), 0)

        expected_fields = [
            'id',
            'created',
            'created_by',
            'created_by_name',
            'modified',
            'name',
            'client_name',
            'parent',
            'description',
            'xform_title',
            'xform_id_string',
            'approved_submissions_count',
            'pending_submissions_count',
            'required_expertise_display',
            'rejected_submissions_count',
            'total_bounty_payout',
            'current_bounty_amount',
            'bounty',
            'start',
            'required_expertise',
            'client',
            'end',
            'status_display',
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
            'task_locations',
            'xform_ona_id',
            'xform_project_id',
            'xform_version',
            'xform_owner',
            'xform_owner_url',
        ]
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))

    def test_start_end_and_timing_rule(self):
        """
        Test start, end and timing rule
        """
        rrule = 'DTSTART:20180521T210000Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=5'

        # when just rrule is provided
        data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'timing_rule': rrule,
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        task = serializer_instance.save()
        self.assertEqual('2018-05-21T21:00:00+00:00', task.start.isoformat())
        self.assertEqual(
            '2018-05-25T23:59:59.999999+00:00', task.end.isoformat())

        # when start and rrule are provided
        data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'timing_rule': rrule,
            'start': '2018-04-21T07:00:00+03:00',
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        task = serializer_instance.save()
        self.assertEqual('2018-04-21T07:00:00+03:00', task.start.isoformat())
        self.assertEqual(
            '2018-05-25T23:59:59.999999+00:00', task.end.isoformat())

        # when end and rrule are provided
        data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'timing_rule': rrule,
            'end': '2019-05-21T07:00:00+03:00',
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        task = serializer_instance.save()
        self.assertEqual('2018-05-21T21:00:00+00:00', task.start.isoformat())
        self.assertEqual(
            '2019-05-21T07:00:00+03:00', task.end.isoformat())

        # when end is less than start
        data = {
            "type": "Task",
            'name': 'Cow price',
            'start': '2018-05-21T07:00:00+03:00',
            'end': '2018-04-21T07:00:00+03:00',
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'timing_rule': rrule,
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            "The end date cannnot be lesser than the start date.",
            str(
                serializer_instance.errors['end'][0]
            )
        )

        # when no start and no timing rule
        data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
        msg = "Cannot determine the start date.  Please provide either the start date or timing rule(s)"  # noqa
        self.assertEqual(
            msg,
            str(
                serializer_instance.errors['timing_rule'][0]
            )
        )
        self.assertEqual(
            msg,
            str(
                serializer_instance.errors['start'][0]
            )
        )
        self.assertEqual(
            msg,
            str(
                serializer_instance.errors['locations_input'][0]
            )
        )

    @patch(
        'kaznet.apps.main.serializers.tasks.get_start_end_from_timing_rules')
    def test_start_end_and_timing_rule_bad_rule(self, mock):
        """
        Test start and end when a bad rule is provide
        and by bad we mean one from which we cannot infer start or end
        """
        mock.return_value = (None, None)
        rrule = 'RRULE:FREQ=DAILY;INTERVAL=1;COUNT=5'

        # when start and bad rrule is provided
        data = {
            "type": "Task",
            'name': 'Cow price',
            'start': '2018-05-21T07:00:00+03:00',
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'timing_rule': rrule,
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        task = serializer_instance.save()
        self.assertEqual('2018-05-21T07:00:00+03:00', task.start.isoformat())
        self.assertEqual(None, task.end)

        # when just rrule is provided
        data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'timing_rule': rrule,
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
        msg = "Cannot determine the start date.  Please provide either the start date or timing rule(s)"  # noqa
        self.assertEqual(
            msg,
            str(
                serializer_instance.errors['timing_rule'][0]
            )
        )
        self.assertEqual(
            msg,
            str(
                serializer_instance.errors['start'][0]
            )
        )
        self.assertEqual(
            msg,
            str(
                serializer_instance.errors['locations_input'][0]
            )
        )

    def test_start_end_timing_rule_update(self):
        """
        Test start, end and timing rule when doing an update
        """
        rrule = 'DTSTART:20180521T210000Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=5'

        # when just rrule is provided
        old_task = mommy.make('main.Task')
        data = {
            "type": "Task",
            'name': 'Cow price',
            'target_content_type': self.xform_type.id,
            'timing_rule': rrule,
        }
        serializer_instance = KaznetTaskSerializer(
            data=data, instance=old_task)
        self.assertTrue(serializer_instance.is_valid())
        serializer_instance.save()
        old_task.refresh_from_db()
        self.assertEqual(rrule, old_task.timing_rule)

        # when start is greater than existing end
        old_task = mommy.make('main.Task', end=timezone.now())
        data = {
            "type": "Task",
            'name': 'Cow price',
            'target_content_type': self.xform_type.id,
            'start': (timezone.now() + timedelta(days=7)).isoformat(),
        }
        serializer_instance = KaznetTaskSerializer(
            data=data, instance=old_task)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            "The start date cannnot be greater than the end date",
            str(
                serializer_instance.errors['start'][0]
            )
        )

        # when end is less than existing start
        old_task = mommy.make('main.Task', start=timezone.now())
        data = {
            "type": "Task",
            'name': 'Cow price',
            'target_content_type': self.xform_type.id,
            'end': (timezone.now() - timedelta(days=7)).isoformat(),
        }
        serializer_instance = KaznetTaskSerializer(
            data=data, instance=old_task)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            "The end date cannnot be lesser than the start date.",
            str(
                serializer_instance.errors['end'][0]
            )
        )

    def test_auto_schedule(self):
        """
        Test that tasks with future dates are auto-scheduled
        """
        data = {
            "type": "Task",
            'name': 'Cow price',
            'start': (timezone.now() + timedelta(days=17)).isoformat(),
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'target_id': mommy.make('ona.XForm').id,
            'status': Task.ACTIVE
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        task = serializer_instance.save()
        self.assertEqual(Task.SCHEDULED, task.status)

    def test_stale_task_active(self):
        """
        Test that tasks with past dates are not allowed when the status
        is acive
        """
        # not allowed when status is active
        data = {
            "type": "Task",
            'name': 'Coconut Quest',
            'start': (timezone.now() - timedelta(days=17)).isoformat(),
            'end': (timezone.now() - timedelta(days=7)).isoformat(),
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'target_id': mommy.make('ona.XForm').id,
            'status': Task.ACTIVE
        }
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            "Cannot create an active task with an end date from the past.",
            str(
                serializer_instance.errors['end'][0]
            )
        )

    def test_auto_draft(self):
        """
        Test that tasks with no XForms are auto-drafted
        """
        data = {
            "type": "Task",
            'name': 'Cow price',
            'start': "2018-05-21T07:00:00+03:00",
            'description': 'Some description',
            'target_content_type': self.xform_type.id,
            'status': Task.ACTIVE
        }  # notice no XForm is supplied
        serializer_instance = KaznetTaskSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        task = serializer_instance.save()
        self.assertEqual(Task.DRAFT, task.status)

    def test_create_task_with_bounty(self):
        """
        Test that a bounty is created if Task is passed into
        KaznetTaskSerializer
        """
        mocked_target_object = mommy.make('ona.XForm')

        rrule = 'DTSTART:20180521T210000Z RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'

        initial_data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'total_submission_target': 10,
            'timing_rule': rrule,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'estimated_time': 'P4DT1H15M20S',
            'amount': '5400'
        }
        with self.settings(KAZNET_DEFAULT_CURRENCY='KES'):
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
            bounty2 = Bounty.objects.get(
                amount=Money('10000000.00', 'KES'))

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
            "type": "Task",
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

    def test_task_start(self):
        """
        Test how the task start is set
        """
        mocked_target_object = mommy.make('ona.XForm')
        rrule1 = 'DTSTART:20180521T210000Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=50'  # noqa
        rrule2 = 'DTSTART:20190521T210000Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=50'  # noqa

        # no timing rule provided
        data1 = {
            "type": "Task",
            'name': 'Coconut One',
            'description': 'Some description',
            'total_submission_target': 1,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'estimated_time': '15:00:00',
            'amount': '5400',
            'start': '2018-06-12T17:48:34+03:00'
        }
        serializer_instance1 = KaznetTaskSerializer(data=data1)
        self.assertTrue(serializer_instance1.is_valid())
        serializer_instance1.save()
        result1 = serializer_instance1.data
        self.assertEqual("2018-06-12T17:48:34+03:00", result1['start'])

        # start > timing rule dtstart
        data2 = {
            "type": "Task",
            'name': 'Coconut One',
            'description': 'Some description',
            'total_submission_target': 1,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'estimated_time': '15:00:00',
            'amount': '5400',
            'start': '2018-05-30T17:48:34+03:00',
            'timing_rule': rrule1
        }
        serializer_instance2 = KaznetTaskSerializer(data=data2)
        self.assertTrue(serializer_instance2.is_valid())
        serializer_instance2.save()
        result2 = serializer_instance2.data
        self.assertEqual("2018-05-30T17:48:34+03:00", result2['start'])

        # start < timing rule dtstart
        data3 = {
            "type": "Task",
            'name': 'Coconut One',
            'description': 'Some description',
            'total_submission_target': 1,
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'estimated_time': '15:00:00',
            'amount': '5400',
            'start': '2018-07-17T17:48:34+03:00',
            'timing_rule': rrule2
        }
        serializer_instance3 = KaznetTaskSerializer(data=data3)
        self.assertTrue(serializer_instance3.is_valid())
        serializer_instance3.save()
        result3 = serializer_instance3.data
        self.assertEqual("2018-07-17T17:48:34+03:00", result3['start'])

    def test_location_link(self):
        """
        Test the connection of Task and Location
        """
        location = mommy.make('main.location', name='Nairobi', country='KE')
        mocked_target_object = mommy.make('ona.XForm')

        now = timezone.now()

        data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
        }

        data_with_location = data.copy()
        locations_input = [
            {
                "location": {
                    "type": "Location",
                    "id": str(location.id)
                },
                "timing_rule": 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
                "start": '09:00:00',
                "end": '15:00:00'
            }
        ]
        data_with_location['locations_input'] = locations_input

        serializer_instance = KaznetTaskSerializer(data=data_with_location)

        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        self.assertDictContainsSubset(
            locations_input[0], serializer_instance.data['task_locations'][0])

        self.assertEqual(location, task.locations.get(id=location.id))

    def test_validate_locations_input(self):
        """
        Test that locations_input is validated correctly
        """
        mocked_target_object = mommy.make('ona.XForm')

        now = timezone.now()

        data = {
            "type": "Task",
            'name': 'Cow price',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
        }

        data_with_location = data.copy()
        locations_input = [
            {
                "location": {
                    "type": "Location",
                    "id": '0'  # invalid
                },
                "timing_rule": 'invalid',  # invalid
                "start": '99:00:00',  # invalid
                "end": 'kesho'  # invalid
            }
        ]
        data_with_location['locations_input'] = locations_input

        serializer_instance = KaznetTaskSerializer(data=data_with_location)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            'Invalid pk "0" - object does not exist.',
            str(
                serializer_instance.errors['locations_input'][0]['location'][0]
            )
        )
        self.assertEqual(
            'Time has wrong format. Use one of these formats instead: '
            'hh:mm[:ss[.uuuuuu]].',
            str(
                serializer_instance.errors['locations_input'][0]['start'][0]
            )
        )
        self.assertEqual(
            'Time has wrong format. Use one of these formats instead: '
            'hh:mm[:ss[.uuuuuu]].',
            str(
                serializer_instance.errors['locations_input'][0]['end'][0]
            )
        )
        self.assertEqual(
            'Invalid Timing Rule.',
            str(
                serializer_instance.errors[
                    'locations_input'][0]['timing_rule'][0]
            )
        )

    def test_task_parent_link(self):
        """
        Test the connection between a parent and child task
        """
        mocked_parent_task = mommy.make('main.Task', name='Cow Price')
        mocked_target_object = mommy.make('ona.XForm')
        now = timezone.now()

        data = {
            "type": "Task",
            'name': 'Milk Production',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'parent':  {
                "type": "Task",
                "id": mocked_parent_task.id
            }
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
            "type": "Task",
            'name': 'Milk Production',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'client': {
                "type": "Client",
                "id": mocked_client.id
            }
        }

        serializer_instance = KaznetTaskSerializer(data=data)

        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        self.assertEqual(mocked_client, task.client)

    def test_created_by_field(self):
        """
        Test created_by field
        """
        mocked_client = mommy.make('main.Client', name='Knights Order')
        mocked_target_object = mommy.make('ona.XForm')
        now = timezone.now()

        data = {
            "type": "Task",
            'name': 'Milk Production',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
            'client': {
                "type": "Client",
                "id": mocked_client.id
            }
        }

        serializer_instance = KaznetTaskSerializer(data=data)

        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        # no created by
        self.assertEqual(None, task.created_by)
        self.assertEqual('', task.created_by_name)
        self.assertEqual(None, serializer_instance.data['created_by'])
        self.assertEqual('', serializer_instance.data['created_by_name'])

        # add created by and test that it is is seriakized
        cate_user = mommy.make(
            'auth.User', username='cate', first_name='Cate', last_name='Doe')
        task.created_by = cate_user
        task.save()
        serializer_instance2 = KaznetTaskSerializer(instance=task)
        self.assertDictEqual(
            {'type': 'User', 'id': str(cate_user.id)},
            dict(serializer_instance2.data['created_by'])
        )
        self.assertEqual(
            'Cate Doe',
            serializer_instance2.data['created_by_name']
        )

    def test_task_end(self):
        """
        Test:
            - If end_date is in the past and Task is Active
              raise validation error
        """
        data = {
            "type": "Task",
            'name': 'Cow price',
            'status': Task.ACTIVE,
            'target_content_type': self.xform_type.id,
            'start': '2018-07-20T17:48:34+03:00',
            'end': '2018-07-29T17:48:34+03:00',
        }
        serializer_instance = KaznetTaskSerializer(
            data=data)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            PAST_END_DATE,
            str(
                serializer_instance.errors['end'][0]
            )
        )
