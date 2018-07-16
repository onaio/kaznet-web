"""
Test module for TaskLocationSeriliazer
"""
from django.test import TestCase
from model_mommy import mommy

from kaznet.apps.main.serializers import TaskLocationSerializer


class TestTaskLocationSerializer(TestCase):
    """
    Test the TaskLocationSerializer
    """

    def test_create_client(self):
        """
        Test that the serializer can create a TaskLocation
        """

        task_location = mommy.make(
            'main.TaskLocation',
            task=mommy.make('main.Task', name='Coconut'),
            location=mommy.make(
                'main.Location', name='Kile', description='I love oov!'))

        serializer_instance = TaskLocationSerializer(instance=task_location)

        self.assertEqual('Kile', serializer_instance.data['location_name'])
        self.assertEqual(
            'I love oov!', serializer_instance.data['location_description'])

        expected_fields = [
            'task',
            'created',
            'modified',
            'location',
            'location_name',
            'location_description',
            'timing_rule',
            'start',
            'end',
        ]
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
