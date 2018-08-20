"""
Viewsets for users app
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.users.filters import UserProfileOrderingFilter
from kaznet.apps.users.models import UserProfile
from kaznet.apps.users.permissions import IsOwnUserProfileOrAdmin
from kaznet.apps.users.serializers import UserProfileSerializer


# pylint: disable=too-many-ancestors
class UserProfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet class for UserProfiles
    """
    authentication_classes = [
        SessionAuthentication, OnaTempTokenAuthentication, TokenAuthentication
    ]
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnUserProfileOrAdmin]
    filter_backends = [
        DjangoFilterBackend, UserProfileOrderingFilter, filters.SearchFilter
    ]
    filter_fields = ['role', 'expertise', 'ona_username']
    search_fields = [
        'user__first_name', 'user__last_name', 'ona_username', 'user__email',
        'national_id'
    ]
    ordering_fields = [
        'user__first_name', 'user__last_name', 'submission_count', 'created',
        'national_id'
    ]
    queryset = UserProfile.objects.all()  # pylint: disable=no-member

    # pylint: disable=unused-argument
    # pylint: disable=invalid-name
    @action(detail=False)
    def profile(self, request, pk=None):
        """
        Action that returns the Currently logged in Users
        Profile
        """
        if request.user.is_authenticated:
            userprofile = request.user.userprofile
            userprofile_data = self.get_serializer(userprofile).data
            return Response(userprofile_data)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
