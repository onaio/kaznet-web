"""
Test for TaskLocation model
"""
from django.test import TestCase

from model_mommy import mommy


class TestTaskLocation(TestCase):
    """
    Test class for TaskLocation model
    """

    def test_task_location_model_str(self):
        """
        Test the str method on TaskLocation model
        """
        task_location = mommy.make(
            'main.TaskLocation',
            task=mommy.make('main.Task', name='Coconut'),
            location=mommy.make('main.Location', name='Kileleshwa'))
        expected = 'Coconut at Kileleshwa'
        self.assertEqual(expected, task_location.__str__())
