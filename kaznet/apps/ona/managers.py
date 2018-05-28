"""
Manager module for Ona App
"""
from django.db import models


# pylint: disable=too-few-public-methods
class GenericSoftDeleteManager(models.Manager):
    """
    Custom manager for Task
    """

    def __init__(self, *args, **kwargs):
        """
        Custom init method auto sets alive_only attribute
        to True
        """
        self.alive_only = kwargs.pop('alive_only', True)
        super(GenericSoftDeleteManager, self).__init__(
            *args, **kwargs)

    def get_queryset(self):
        """
        Custom get_queryset method for GenericSoftDeleteManger
        """
        queryset = super(GenericSoftDeleteManager, self).get_queryset()

        if self.alive_only:
            return queryset.filter(deleted_at=None)
        return queryset
