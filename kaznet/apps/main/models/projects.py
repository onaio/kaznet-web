"""
Module for the Project model
"""
from django.db import models
from django.utils.translation import ugettext as _

from tasking.models import BaseProject


class Project(BaseProject):
    """
    Project model class
    """
    tasks = models.ManyToManyField(
        'tasking.Task',
        verbose_name=_('Tasks'),
        blank=True,
        default=None,
        help_text=_('This represents the Task.'))

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the Project model
        """
        abstract = False
        ordering = ['name']

    def __str__(self):
        """
        String representation of a Project object

        e.g. Livestock prices
        """
        return self.name
