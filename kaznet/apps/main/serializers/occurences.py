"""
Main Occurrences Serializer module
"""
from tasking.serializers import TaskOccurrenceSerializer

from kaznet.apps.main.models import TaskOccurrence


class KaznetTaskOccurrenceSerializer(TaskOccurrenceSerializer):
    """
    Main Occurence Serializer
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for KaznetTaskOccurrenceSerializer
        """
        model = TaskOccurrence
        fields = [
            'id',
            'task',
            'created',
            'modified',
            'date',
            'start_time',
            'end_time',
            'time_string'
        ]
