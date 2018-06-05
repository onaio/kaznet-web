"""
Tests for main signals
"""

from django.test import TestCase

from model_mommy import mommy

from kaznet.apps.main.models import TaskOccurrence
from kaznet.apps.main.models import Submission
from django.utils import timezone

class TestSignals(TestCase):
    """
    Tests for Kanzet app signals
    """
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

    def test_create_submissions(self):
        """
        Check that a kaznet submission is created when an ona
        submission is made
        """
        ona_form = mommy.make('ona.XForm')
        user=mommy.make('auth.User')
        puppy_task=mommy.make(
            'main.Task',
            name='Puppy Prices',
            target_content_object = ona_form
        )
        bounty = mommy.make('main.Bounty', task=puppy_task)
        submission = mommy.make(
            'ona.OnaInstance',
            xform=ona_form,
            # TODO: make sure JSON data from ONA is saved in a consistent way
            # TODO: add user field to ona submission
            json=dict(submission_time=timezone.now().isoformat(), user_id=user.id)
        )

        self.assertEqual(1, Submission.objects.filter(task=puppy_task).count())
