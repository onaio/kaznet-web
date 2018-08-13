"""
Location Type viewsets
"""

from rest_framework import filters, mixins, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.main.models import LocationType
from kaznet.apps.main.serializers import KaznetLocationTypeSerializer
from kaznet.apps.users.permissions import IsAdminOrReadOnly


# pylint: disable=too-many-ancestors
class KaznetLocationTypeViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin,
        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for LocationTypes
    """
    authentication_classes = [
        OnaTempTokenAuthentication,
        SessionAuthentication,
        TokenAuthentication
        ]
    serializer_class = KaznetLocationTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['name']
    ordering_fields = ['name', 'created']
    queryset = LocationType.objects.all()  # pylint: disable=no-member
