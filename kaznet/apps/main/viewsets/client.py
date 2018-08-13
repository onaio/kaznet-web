"""
Client viewset module
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.main.models import Client
from kaznet.apps.main.serializers import ClientSerializer
from kaznet.apps.users.permissions import IsAdmin


# pylint: disable=too-many-ancestors
class ClientViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Client ViewSet
    """
    authentication_classes = [
        SessionAuthentication,
        OnaTempTokenAuthentication,
        TokenAuthentication
        ]
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = [
        'name',
    ]
    queryset = Client.objects.all()  # pylint: disable=no-member
