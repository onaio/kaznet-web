"""
Module for Main app utils tests
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from dateutil.rrule import rrulestr
from model_mommy import mommy
from tasking.utils import get_rrule_end, get_rrule_start

from kaznet.apps.main.models import TaskOccurrence
from kaznet.apps.main.utils import (create_occurrences,
                                    get_start_end_from_timing_rules)


class TestUtils(TestCase):
    """
    Tests for Kanzet app utils
    """

    def test_get_start_end_from_timing_rules(self):
        """
        Test get_start_end_from_timing_rules
        """
        zero = ['invalid']
        one = [None]
        two = []
        three = [None, 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5']
        four = [
            'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=17',
            'DTSTART:20170521T210000Z RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'
        ]

        self.assertEqual(
            (None, None),
            get_start_end_from_timing_rules(zero)
        )
        self.assertEqual(
            (None, None),
            get_start_end_from_timing_rules(one)
        )
        self.assertEqual(
            (None, None),
            get_start_end_from_timing_rules(two)
        )
        self.assertEqual(
            (
                get_rrule_start(
                    rrulestr('RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')
                ),
                get_rrule_end(
                    rrulestr('RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5')
                )
            ),
            get_start_end_from_timing_rules(three)
        )
        self.assertEqual(
            (
                get_rrule_start(
                    rrulestr(
                        'DTSTART:20170521T210000Z RRULE:FREQ=DAILY;COUNT=5')
                ),
                get_rrule_end(
                    rrulestr('RRULE:FREQ=DAILY;INTERVAL=10;COUNT=17')
                )
            ),
            get_start_end_from_timing_rules(four)
        )

    def test_create_occurrences(self):
        """
        Test create_occurrences
        """
        # test future occurrences
        future = timezone.now() + timedelta(days=10)
        task = mommy.make(
            'main.Task',
            name="Oov",
            timing_rule=f'DTSTART:{future.isoformat()} RRULE:FREQ=DAILY;INTERVAL=1;COUNT=17')  # noqa

        create_occurrences(task)
        # pylint: disable=no-member
        self.assertEqual(17, TaskOccurrence.objects.filter(task=task).count())

        # test when occurrences in the past exist
        task2 = mommy.make(
            'main.Task',
            name="Oov",
            timing_rule=f'DTSTART:{future.isoformat()} RRULE:FREQ=DAILY;INTERVAL=1;COUNT=3')  # noqa
        mommy.make(
            'main.TaskOccurrence',
            task=task2,
            date=timezone.now() - timedelta(days=10),  # past
        )
        mommy.make(
            'main.TaskOccurrence',
            task=task2,
            date=timezone.now() + timedelta(days=45),  # future
        )
        create_occurrences(task2)
        # we should keep the occurrence in the past
        # pylint: disable=no-member
        self.assertEqual(4, TaskOccurrence.objects.filter(task=task2).count())

        # test when we have task location occurrences
        task3 = mommy.make(
            'main.Task',
            name="Coco",
            timing_rule=None)  # noqa
        mommy.make(
            'main.TaskOccurrence',
            task=task3,
            date=timezone.now() - timedelta(days=10),  # past
        )
        mommy.make(
            'main.TaskOccurrence',
            task=task3,
            date=timezone.now() + timedelta(days=45),  # future
        )
        mommy.make(
            'main.TaskLocation',
            task=task3,
            location=mommy.make('main.Location'),
            timing_rule=f'DTSTART:{future.isoformat()} RRULE:FREQ=DAILY;INTERVAL=1;COUNT=7',  # noqa
            start="09:00:00",
            end="16:00:00"
        )
        create_occurrences(task3)
        # we should keep the occurrence in the past
        # pylint: disable=no-member
        self.assertEqual(8, TaskOccurrence.objects.filter(task=task3).count())

        # test when we have no timing_rule
        task4 = mommy.make(
            'main.Task',
            name="Pearlz",
            timing_rule=None)
        mommy.make(
            'main.TaskOccurrence',
            task=task4,
            date=timezone.now() - timedelta(days=10),  # past
        )
        mommy.make(
            'main.TaskOccurrence',
            task=task4,
            date=timezone.now() + timedelta(days=45),  # future
        )
        create_occurrences(task4)
        # we should keep the occurrence in the past
        # pylint: disable=no-member
        self.assertEqual(0, TaskOccurrence.objects.filter(task=task4).count())