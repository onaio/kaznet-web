"""
Viewsets for users app
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.users.models import UserProfile
from kaznet.apps.users.serializers import UserProfileSerializer


# pylint: disable=too-many-ancestors
class UserProfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet class for UserProfiles
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter]
    search_fields = [
        'user__first_name', 'user__last_name', 'ona_username',
        'user__email', 'national_id']
    ordering_fields = [
        'user__first_name', 'user__last_name', 'submission_count', 'created',
        'national_id']
    queryset = UserProfile.objects.first()  # pylint: disable=no-member
