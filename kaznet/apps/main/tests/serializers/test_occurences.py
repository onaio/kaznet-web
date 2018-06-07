"""
Test for KaznetTaskOccurrenceSerializer
"""

from model_mommy import mommy
from kaznet.apps.main.tests.base import MainTestBase

from kaznet.apps.main.serializers import KaznetTaskOccurenceSerializer


class TestTaskOccurrenceSerializer(MainTestBase):
    """
    Test the TaskOccurrenceSerializer
    """

    def test_create_occurrence(self):
        """
        Test that the serializer can create TaskOccurrence objects
        """

        task = mommy.make('main.Task')

        data = {
            'task': task.id,
            'date': '2018-05-24',
            'start_time': '07:00:00',
            'end_time': '19:00:00'
        }

        serializer_instance = KaznetTaskOccurenceSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        occurrence = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual(
            occurrence.task.id, serializer_instance.data['task'])
        self.assertEqual(
            '24th May 2018, 7 a.m. to 7 p.m.',
            serializer_instance.data['time_string'])

        expected_fields = [
            'created',
            'modified',
            'task',
            'start_time',
            'date',
            'end_time',
            'time_string',
            'id',
        ]
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data)))
