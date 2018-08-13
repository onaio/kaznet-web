"""
Viewsets for users app
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from kaznet.apps.users.filters import UserProfileOrderingFilter
from kaznet.apps.users.models import UserProfile
from kaznet.apps.users.permissions import IsAdmin, IsOwnUserProfileOrAdmin
from kaznet.apps.users.serializers import UserProfileSerializer
from kaznet.apps.users.api import create_ona_user


# pylint: disable=too-many-ancestors
class UserProfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet class for UserProfiles
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = UserProfileSerializer
    permission_classes = [
        IsAuthenticated, IsOwnUserProfileOrAdmin]
    filter_backends = [
        DjangoFilterBackend,
        UserProfileOrderingFilter,
        filters.SearchFilter]
    filter_fields = ['role', 'expertise']
    search_fields = [
        'user__first_name', 'user__last_name', 'ona_username',
        'user__email', 'national_id']
    ordering_fields = [
        'user__first_name', 'user__last_name', 'submission_count', 'created',
        'national_id']
    queryset = UserProfile.objects.all()  # pylint: disable=no-member

    @action(methods=['post'], detail=False, permission_classes=[IsAdmin])
    def create_user_ona(self, request):
        """
        Action that creates a user on Ona and then creates
        A Kaznet User
        """
        serializer_instance = self.get_serializer(data=request.data)
        username = request.data.get('ona_username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')

        if serializer_instance.is_valid():
            created, errors = create_ona_user(
                username,
                first_name,
                last_name,
                email,
                password
            )

            if created:
                serializer_instance.save()
                return Response(
                    serializer_instance.data,
                    status=status.HTTP_201_CREATED)

            return Response(
                errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
