"""
Tests for celery tasks
"""
from unittest.mock import patch

from django.test import TestCase

from model_mommy import mommy

from kaznet.apps.main.tasks import task_create_occurrences


@patch('kaznet.apps.main.tasks.create_occurrences')
class TestCeleryTasks(TestCase):
    """
    Tests for celery tasks
    """

    def test_task_create_occurrences(self, mock):
        """
        Test task_create_occurrences
        """
        task = mommy.make("main.Task")
        task_create_occurrences(task_id=task.id)
        mock.assert_called_with(task)
