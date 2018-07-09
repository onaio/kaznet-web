"""
Module for Main app utils tests
"""

from django.test import TestCase

from dateutil.rrule import rrulestr
from tasking.utils import get_rrule_end, get_rrule_start

from kaznet.apps.main.utils import get_start_end_from_timing_rules


class TestSignals(TestCase):
    """
    Tests for Kanzet app signals
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
