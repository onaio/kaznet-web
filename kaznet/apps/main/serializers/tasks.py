"""
Main Tasks serializer module
"""
from tasking.serializers import TaskSerializer

from kaznet.apps.main.models import Task


class KaznetTaskSerializer(TaskSerializer):
    """
    Main Task Serializer class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for KaznetTaskSerializer
        """
        fields = [
            'id',
            'created',
            'modified',
            'name',
            'parent',
            'estimated_time',
            'description',
            'start',
            'end',
            'timing_rule',
            'total_submission_target',
            'user_submission_target',
            'status',
            'submission_count',
            'target_content_type',
            'target_id',
            'segment_rules',
            'locations',
        ]

        model = Task
