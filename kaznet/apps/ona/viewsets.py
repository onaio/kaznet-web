"""
Viewsets for Ona app Models
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.mixins import KaznetViewsetMixin
from kaznet.apps.ona.filters import XFormFilterSet
from kaznet.apps.ona.models import XForm
from kaznet.apps.ona.serializers import XFormSerializer
from kaznet.apps.users.permissions import IsAdmin


# pylint: disable=too-many-ancestors
class XFormViewSet(KaznetViewsetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Read Only Viewset for XFormViewSet
    """
    filter_backends = [
        filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filter_class = XFormFilterSet
    serializer_class = XFormSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    search_fields = ['title']
    ordering_fields = ['title', 'modified']
    queryset = XForm.objects.all()  # pylint: disable=no-member
