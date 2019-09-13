"""
Tests for main signals
"""
from unittest.mock import patch

from django.test import override_settings
from django.utils import timezone
from model_mommy import mommy

from kaznet.apps.main.models import Submission, TaskOccurrence
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.tests.test_celery_tasks import MOCKED_INSTANCES


class TestSignals(MainTestBase):
    """
    Tests for Kanzet app signals
    """

    def setUp(self):
        super().setUp()
        self.user = mommy.make(
            'auth.User',
            username='sluggie'
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_task_occurrences(self):
        """
        Test that task occurrences are created when a new Task object is
        created
        """
        # create a Task object
        task = mommy.make(
            'main.Task',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=1;COUNT=57')

        # pylint: disable=no-member
        self.assertEqual(57, TaskOccurrence.objects.filter(task=task).count())

    @patch('kaznet.apps.main.signals.task_create_occurrences.delay')
    def test_create_occurrences_signal_handler(self, mock):
        """
        Test create_occurrences signal handler
        """
        task = mommy.make(
            'main.Task',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=1;COUNT=57')
        # the celery task should have been called
        self.assertEqual(1, mock.call_count)
        mock.assert_called_with(task_id=task.id)

        task.timing_rule = 'RRULE:FREQ=DAILY;INTERVAL=1;COUNT=7'
        task.save()
        # the celery task should have been called again
        self.assertEqual(2, mock.call_count)
        mock.assert_called_with(task_id=task.id)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_create_submissions(self):
        """
        Check that a kaznet submission is created when an ona
        submission is made
        """
        mommy.make('auth.User', username='onasupport')
        ona_form = mommy.make('ona.XForm')
        puppy_task = mommy.make(
            'main.Task',
            name='Puppy Prices',
            target_content_object=ona_form
        )
        mommy.make(
            'ona.Instance',
            xform=ona_form,
            json=MOCKED_INSTANCES[1]
        )
        self.assertEqual(1, Submission.objects.filter(task=puppy_task).count())

        # when dict is empty fail silently
        mommy.make(
            'ona.Instance',
            xform=ona_form,
            json=dict
        )
        self.assertEqual(1, Submission.objects.filter(task=puppy_task).count())

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_create_submission_for_missing_task(self):
        """
        check that an AttributeError exception occures when
        a submission is created for an xform that does not
        have a task
        """
        # assert that the messaged is logged
        with self.assertLogs(logger="submission logger",
                             level='ERROR') as log_messages:
            mommy.make('auth.User', username='onasupport')
            # create an xform but no task
            ona_form = mommy.make('ona.XForm')
            puppy_task = mommy.make(
                'main.Task',
                name='Puppy Prices',
                target_content_object=ona_form
            )
            puppy_task.delete()
            # create an instance for this form(ona_form)
            mommy.make(
                'ona.Instance',
                xform=ona_form,
                json=dict
            )
            self.assertIn(
                'ERROR:submission logger:Instance: 1"\
                    "belongs to a task that has been deleted',
                log_messages.output
            )

    @patch('kaznet.apps.main.signals.task_create_submission.delay')
    def test_create_submission_signal_handler(self, mock):
        """
        Test create_submission signal handler
        """
        ona_form = mommy.make('ona.XForm')
        instance = mommy.make(
            'ona.Instance',
            xform=ona_form,
            user=self.user,
            json=dict(submission_time=timezone.now().isoformat())
        )
        # the celery task should have been called
        self.assertEqual(1, mock.call_count)
        mock.assert_called_with(instance_id=instance.id)

        instance.save()
        # the celery task should have been called again
        self.assertEqual(2, mock.call_count)
        mock.assert_called_with(instance_id=instance.id)
