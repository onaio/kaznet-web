"""
Test for TaskLocation model
"""
from django.test import TestCase

from model_mommy import mommy


class TestTaskLocation(TestCase):
    """
    Test class for TaskLocation model
    """

    def test_tasklocation_model_str(self):
        """
        Test the str method on TaskLocation model
        """
        task = mommy.make('main.Task', name='SpaceShip Price')
        location = mommy.make('main.Location', name='Sol Stone')
        tasklocation = mommy.make(
            'main.TaskLocation', task=task, location=location)
        expected = f'Task Location for Task: {task}, Submission: {location}'
        self.assertEqual(expected, tasklocation.__str__())
