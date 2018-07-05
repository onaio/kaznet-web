"""
Main TaskLocation serializer module
"""
from rest_framework_json_api import serializers
from tasking.serializers.task import check_timing_rule

from kaznet.apps.main.models import TaskLocation


# pylint: disable=too-many-ancestors
class TaskLocationSerializer(serializers.ModelSerializer):
    """
    TaskLocation serialzier class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskLocationSerializer
        """
        model = TaskLocation
        fields = [
            'task',
            'created',
            'modified',
            'location',
            'timing_rule',
            'start',
            'end'
        ]

    # pylint: disable=no-self-use
    def validate_timing_rule(self, value):
        """
        Validate timing rule
        """
        return check_timing_rule(value)


# pylint: disable=too-many-ancestors
class TaskLocationCreateSerializer(TaskLocationSerializer):
    """
    Serializer model class used when creating a TaskLocation object
    during Task creation
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskLocationSerializer
        """
        model = TaskLocation
        # we dont include the task field as it will be added in TaskSerializer
        fields = [
            'location',
            'timing_rule',
            'start',
            'end'
        ]

    def to_representation(self, instance):
        """
        Use TaskLocationSerializer when reading the object
        """
        return TaskLocationSerializer(instance).data
