"""
Manager module for Kaznet main app
"""
from django.db import models


# pylint: disable=too-few-public-methods
class TaskManager(models.Manager):
    """
    Custom manager for main.Task
    """

    def get_queryset(self):
        """
        Custom get_queryset method
        """
        queryset = super().get_queryset()
        # add submission count to queryset as annotation
        queryset = queryset.annotate(
            submission_count=models.Count('submission__id'))
        return queryset


class SubmissionManager(models.Manager):
    """
    Manager to help in filtering submissions
    """
    def approved(self):
        """Return approved submissions"""
        return self.filter(status='a')

    def rejected(self):
        """Return rejected submissions"""
        return self.filter(status='b')

    def under_review(self):
        """Return submissions under review"""
        return self.filter(status='c')

    def pending(self):
        """Return pending submissions"""
        return self.filter(status='d')
