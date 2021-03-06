"""
Main Location viewsets
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.filters import KaznetLocationFilterSet
from kaznet.apps.main.mixins import KaznetViewsetMixin
from kaznet.apps.main.models import Location
from kaznet.apps.main.serializers import KaznetLocationSerializer
from kaznet.apps.users.permissions import IsAdminOrReadOnly


# pylint: disable=too-many-ancestors
class KaznetLocationViewSet(KaznetViewsetMixin, mixins.CreateModelMixin,
                            mixins.ListModelMixin, mixins.UpdateModelMixin,
                            viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin):
    """
    Viewset for Location
    """
    serializer_class = KaznetLocationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filter_class = KaznetLocationFilterSet
    search_fields = ['name']
    ordering_fields = ['name', 'created', 'modified']
    queryset = Location.objects.all()
