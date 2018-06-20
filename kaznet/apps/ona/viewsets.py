"""
Viewsets for Ona app Models
"""
from rest_framework import viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.ona.models import XForm
from kaznet.apps.ona.serializers import XFormSerializer
from kaznet.apps.users.permissions import IsAdmin


# pylint: disable=too-many-ancestors
class XFormViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Viewset for XFormViewSet
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = XFormSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = XForm.objects.all()  # pylint: disable=no-member
