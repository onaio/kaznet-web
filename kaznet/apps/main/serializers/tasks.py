"""
Main Tasks serializer module
"""
from tasking.serializers import TaskSerializer

from kaznet.apps.main.models import Task


class KaznetTaskSerializer(TaskSerializer):
    """
    Main Task Serializer class
    """
    model = Task
