"""
Module for SegmentRule model(s)
"""
from tasking.models import BaseSegmentRule


class SegmentRule(BaseSegmentRule):
    """
    SegmentRule model class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for SegmentRule
        """
        abstract = False
        app_label = 'main'
        ordering = ['name']

    def __str__(self):
        return self.name
