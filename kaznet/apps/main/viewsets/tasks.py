"""
Main Tasks viewset module
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.filters import KaznetTaskFilterSet
from kaznet.apps.main.models import Task
from kaznet.apps.main.serializers import KaznetTaskSerializer
from kaznet.apps.users.permissions import IsAdminOrReadOnly


# pylint: disable=too-many-ancestors
class KaznetTaskViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Main Task Viewset class
    """
    serializer_class = KaznetTaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter]
    filter_class = KaznetTaskFilterSet
    search_fields = ['name']
    ordering_fields = [
        'created',
        'status',
        'estimated_time',
        'submission_count',
        'project__id',
        'name'
    ]
    queryset = Task.with_submission_count.all()
