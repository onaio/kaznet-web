"""
Test for TaskLocation model
"""
from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase


class TestTaskLocation(MainTestBase):
    """
    Test class for TaskLocation model
    """

    def setUp(self):
        super().setUp()

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

    def test_task_location_location_name(self):
        """
        Test the location_name property on TaskLocation model
        """
        task_location = mommy.make(
            'main.TaskLocation',
            task=mommy.make('main.Task', name='Coconut'),
            location=mommy.make('main.Location', name='Kileleshwa'))
        self.assertEqual('Kileleshwa', task_location.location_name)

    def test_task_location_location_description(self):
        """
        Test the location_description property on TaskLocation model
        """
        task_location = mommy.make(
            'main.TaskLocation',
            task=mommy.make('main.Task', name='Coconut'),
            location=mommy.make(
                'main.Location', name='Kile', description='I love oov!'))
        self.assertEqual('I love oov!', task_location.location_description)
