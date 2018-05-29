"""
Module for the Task model(s)
"""
from django.db import models
from django.utils.translation import ugettext as _

from tasking.models import BaseTask
from tasking.models.managers import TaskManager


class Task(BaseTask):
    """
    Task model class
    """
    segment_rules = models.ManyToManyField(
        'tasking.SegmentRule',
        verbose_name=_('Segment Rules'),
        blank=True,
        default=None
    )
    locations = models.ManyToManyField(
        'tasking.Location',
        verbose_name=_('Location'),
        blank=True,
        default=None,
        help_text=_('This represents the location.'))

    # Custom Manager that has submission_count field
    with_submission_count = TaskManager()

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the Task model
        """
        abstract = False
        ordering = ['start', 'name', 'id']

    def __str__(self):
        """
        String representation of a Task object

        e.g. Cow prices - 1
        """
        return "{name} - {pk}".format(pk=self.pk, name=self.name)

    # pylint: disable=no-member
    def get_submissions(self):
        """
        Custom method to get number of submissions
        """
        return self.submission_set.count()

    @property
    def submissions(self):
        """
        Number of Submissions made for this task
        """
        return self.get_submissions()
