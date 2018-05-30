"""
Tests for main signals
"""

from django.test import TestCase

from model_mommy import mommy

from kaznet.apps.main.models import TaskOccurrence


class TestSignals(TestCase):
    def test_task_occurrences(self):
        """
        Test that task occurrences are created when a new Task object is
        created
        """
        # create a Task object
        task = mommy.make(
            'main.Task',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=57')

        # pylint: disable=no-member
        self.assertEqual(57, TaskOccurrence.objects.filter(task=task).count())
