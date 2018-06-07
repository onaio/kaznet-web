"""
Main Occurence ViewSet Module
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.models import TaskOccurrence
from kaznet.apps.main.serializers import KaznetTaskOccurrenceSerializer
from kaznet.apps.main.filters import KaznetTaskOccurrenceFilterSet

from kaznet.apps.users.permissions import IsAdmin


# pylint: disable=too-many-ancestors
class KaznetTaskOccurrenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for occurrence
    """
    serializer_class = KaznetTaskOccurrenceSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_class = KaznetTaskOccurrenceFilterSet
    ordering_fields = [
        'created',
        'date',
        'start_time',
        'end_time']
    queryset = TaskOccurrence.objects.all()  # pylint: disable=no-member
