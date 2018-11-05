"""
Tests for ona signals
"""
from unittest.mock import patch

from django.test import TestCase

from model_mommy import mommy


class TestSignals(TestCase):
    """
    Tests for ona app signals
    """

    def setUp(self):
        self.user = mommy.make(
            'auth.User',
            username='sluggie'
        )

    @patch('kaznet.apps.ona.signals.task_create_form_webhook.delay')
    @patch(
        'kaznet.apps.ona.signals.task_auto_create_filtered_data_sets.delay')
    def test_auto_create_filtered_data_sets_signal_handler(self, mock, mock2):
        """
        Test auto create filtered data sets signal handler
        """
        ona_form = mommy.make(
            'ona.XForm',
            ona_pk=100,
            ona_project_id=1542,
            title='Test Form'
        )

        # the celery task should have been called
        self.assertEqual(1, mock.call_count)
        mock.assert_called_with(
            form_id=ona_form.ona_pk,
            project_id=ona_form.ona_project_id,
            form_title=ona_form.title)

    @patch(
        'kaznet.apps.ona.signals.task_auto_create_filtered_data_sets.delay')
    @patch('kaznet.apps.ona.signals.task_create_form_webhook.delay')
    def test_create_form_webhook_signal(self, mock, mock2):
        """
        Test create_form_webhook_signal handler
        """
        ona_form = mommy.make(
            'ona.XForm',
            ona_pk=101,
            ona_project_id=1543,
            title='Test Form'
        )
        # the celery task should have been called
        self.assertEqual(1, mock.call_count)
        mock.assert_called_with(form_id=ona_form.ona_pk)
