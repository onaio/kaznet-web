"""
ContentType ViewSet
"""

from rest_framework import viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.main.serializers import KaznetContentTypeSerializer


# pylint: disable=too-many-ancestors
class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Viewset for ContentType
    """
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        OnaTempTokenAuthentication]
    serializer_class = KaznetContentTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = get_allowed_contenttypes()

    def get_queryset(self):
        queryset = super(ContentTypeViewSet, self).get_queryset()
        return queryset.order_by('app_label', 'model')
