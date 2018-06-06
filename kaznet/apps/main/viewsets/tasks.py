"""
Main Tasks viewset module
"""
from rest_framework.permissions import IsAuthenticated
from tasking.viewsets import TaskViewSet

from kaznet.apps.main.models import Task
from kaznet.apps.main.serializers import KaznetTaskSerializer
from kaznet.apps.users.permissions import IsAdminOrReadOnly


class KaznetTaskViewSet(TaskViewSet):
    """
    Main Task Viewset class
    """
    serializer_class = KaznetTaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Task.with_submission_count.all()
