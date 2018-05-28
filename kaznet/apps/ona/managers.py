"""
Manager module for Ona App
"""
from django.db import models


# pylint: disable=too-few-public-methods
class GenericSoftDeleteManager(models.Manager):
    """
    Custom manager for Task
    """

    def alive_only(self):
        """
        Custom Method that returns a queryset of Non-Deleted
        Objects
        """
        queryset = super(GenericSoftDeleteManager, self).get_queryset()
        return queryset.filter(deleted_at=None)
