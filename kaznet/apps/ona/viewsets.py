"""
Viewsets for Ona app Models
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.ona.serializers import XFormSerializer
from kaznet.apps.ona.models import XForm


class XFormViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Viewset for XFormViewSet
    """

    serializer_class = XFormSerializer
    permission_classes = IsAuthenticated
    queryset = XForm.objects.all()
