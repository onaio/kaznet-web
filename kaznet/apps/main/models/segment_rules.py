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
        ordering = ['name']
        app_label = 'main'

    def __str__(self):
        return self.name
