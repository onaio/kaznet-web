"""
Tests for celery tasks
"""
from datetime import date, timedelta
from unittest.mock import patch

from django.utils import timezone
from model_mommy import mommy

from kaznet.apps.main.models import Task, TaskOccurrence
from kaznet.apps.main.tasks import (task_create_occurrences,
                                    task_create_submission,
                                    task_has_no_more_occurences,
                                    task_past_end_date)
from kaznet.apps.main.tests.base import MainTestBase


class TestCeleryTasks(MainTestBase):
    """
    Tests for celery tasks
    """

    def setUp(self):
        super().setUp()

    @patch('kaznet.apps.main.tasks.create_occurrences')
    def test_task_create_occurrences(self, mock):
        """
        Test task_create_occurrences
        """
        task = mommy.make("main.Task")
        task_create_occurrences(task_id=task.id)
        mock.assert_called_with(task)

    @patch('kaznet.apps.main.tasks.create_submission')
    def test_task_create_submission(self, mock):
        """
        Test task_task_create_submission
        """
        instance = mommy.make("ona.Instance")
        task_create_submission(instance_id=instance.id)
        mock.assert_called_with(ona_instance=instance)

    def test_task_past_end_date(self):
        """
        Test task_set_end_date
        """
        task1 = mommy.make(
            "main.Task", status=Task.ACTIVE,
            end=timezone.now() - timezone.timedelta(days=1))
        task2 = mommy.make(
            "main.Task", status=Task.EXPIRED,
            end=timezone.now() - timezone.timedelta(days=1))
        task3 = mommy.make(
            "main.Task", status=Task.ACTIVE,
            end=timezone.now() + timezone.timedelta(days=1))
        task_past_end_date()
        task1.refresh_from_db()
        task2.refresh_from_db()
        task3.refresh_from_db()
        self.assertEqual(Task.EXPIRED, task1.status)
        self.assertEqual(Task.EXPIRED, task2.status)
        self.assertEqual(Task.ACTIVE, task3.status)

    def test_task_has_no_more_occurences(self):
        """
        Test Task_has_no_more_occurences
        """
        # all occurences in the past
        task = mommy.make(
            "main.Task", status=Task.ACTIVE,
            name="Other Food Commodity Prices",
            end=timezone.now() + timezone.timedelta(days=1))
        # pylint: disable=no-member
        TaskOccurrence.objects.filter(task=task).delete()
        mommy.make(
            "main.TaskOccurrence",
            date=date.today() - timedelta(days=1), task=task)
        mommy.make(
            "main.TaskOccurrence",
            date=date.today() - timedelta(days=1), task=task)
        # all occurences in the future
        task1 = mommy.make(
            "main.Task", status=Task.ACTIVE,
            name="Cows head count",
            end=timezone.now() + timezone.timedelta(days=1))
        # pylint: disable=no-member
        TaskOccurrence.objects.filter(task=task1).delete()
        mommy.make(
            "main.TaskOccurrence",
            date=date.today() + timedelta(days=1), task=task1)
        mommy.make(
            "main.TaskOccurrence",
            date=date.today() + timedelta(days=1), task=task1)
        # task occurences in the past and the future
        task2 = mommy.make(
            "main.Task", status=Task.ACTIVE,
            name="Goats Distribution",
            end=timezone.now() + timezone.timedelta(days=1))
        # pylint: disable=no-member
        TaskOccurrence.objects.filter(task=task2).delete()
        mommy.make(
            "main.TaskOccurrence",
            date=date.today() - timedelta(days=1), task=task2)
        mommy.make(
            "main.TaskOccurrence",
            date=date.today() + timedelta(days=1), task=task2)
        task_has_no_more_occurences()
        task.refresh_from_db()
        task1.refresh_from_db()
        task2.refresh_from_db()
        self.assertEqual(Task.EXPIRED, task.status)
        self.assertEqual(Task.ACTIVE, task1.status)
        self.assertEqual(Task.ACTIVE, task2.status)
