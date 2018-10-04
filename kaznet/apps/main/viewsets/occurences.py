"""
Main Occurrence ViewSet Module
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.main.filters import KaznetTaskOccurrenceFilterSet
from kaznet.apps.main.models import TaskOccurrence
from kaznet.apps.main.serializers import KaznetTaskOccurrenceSerializer
from kaznet.apps.users.permissions import IsAdmin


# pylint: disable=too-many-ancestors
class KaznetTaskOccurrenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for occurrence
    """
    authentication_classes = [
        OnaTempTokenAuthentication,
        TokenAuthentication,
        SessionAuthentication
        ]
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
