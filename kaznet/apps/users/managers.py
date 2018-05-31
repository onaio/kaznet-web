"""
Manager module for Kaznet main app
"""
from django.db import models


# pylint: disable=too-few-public-methods
class UserProfileManager(models.Manager):
    """
    Custom manager for users.UserProfile
    """

    def get_queryset(self):
        """
        Custom get_queryset method
        """
        queryset = super().get_queryset()
        # add submission count to queryset as annotation
        queryset = queryset.annotate(
            submission_count=models.Count('user__submission__id'))
        return queryset
