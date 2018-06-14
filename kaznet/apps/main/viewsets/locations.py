"""
Main Location viewsets
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.models import Location
from kaznet.apps.main.serializers import KaznetLocationSerializer
from kaznet.apps.users.permissions import IsAdmin


# pylint: disable=too-many-ancestors
class KaznetLocationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                            mixins.UpdateModelMixin, viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin):
    """
    Viewset for Location
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = KaznetLocationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter]
    filter_fields = ['parent', 'country']
    search_fields = ['name']
    ordering_fields = ['name', 'created']
    queryset = Location.objects.all()
