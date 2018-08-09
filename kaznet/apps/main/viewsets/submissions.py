"""
Main Submissions ViewSet Module
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.main.models import Submission
from kaznet.apps.main.serializers import KaznetSubmissionSerializer
from kaznet.apps.users.permissions import IsOwnSubmissionOrAdmin


# pylint: disable=too-many-ancestors
class KaznetSubmissionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Submissions
    """
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        OnaTempTokenAuthentication
        ]
    serializer_class = KaznetSubmissionSerializer
    permission_classes = [IsAuthenticated, IsOwnSubmissionOrAdmin]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = [
        'task',
        'user',
        'location',
        'valid',
        'status'
    ]
    ordering_fields = [
        'bounty__amount',
        'submission_time',
        'task__id'
    ]
    queryset = Submission.objects.all()  # pylint: disable=no-member
