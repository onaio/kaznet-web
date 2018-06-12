"""
Main Occurrences Serializer module
"""
from rest_framework_json_api import serializers

from kaznet.apps.main.models import TaskOccurrence


# pylint: disable=too-many-ancestors
class KaznetTaskOccurrenceSerializer(serializers.ModelSerializer):
    """
    TaskOccurrence serializer class
    """
    time_string = serializers.SerializerMethodField()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskOccurrenceSerializer
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

    # pylint: disable=no-self-use
    def get_time_string(self, obj):
        """
        Returns a friendly human-readable description of the occurrence
        date and times
        """
        return obj.get_timestring()
