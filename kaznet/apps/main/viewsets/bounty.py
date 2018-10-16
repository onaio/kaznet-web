"""
Bounty ViewSet Module
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.mixins import KaznetViewsetMixin
from kaznet.apps.main.models import Bounty
from kaznet.apps.main.serializers import BountySerializer
from kaznet.apps.users.permissions import IsAdmin


# pylint: disable=too-many-ancestors
class BountyViewSet(KaznetViewsetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Bounty ViewSet class
    """
    serializer_class = BountySerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [
        DjangoFilterBackend,
        ]
    filter_fields = ['task_id', 'submission']
    queryset = Bounty.objects.all()  # pylint: disable=no-member
