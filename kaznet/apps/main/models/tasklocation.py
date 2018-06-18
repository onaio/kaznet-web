"""
Module for TaskLocation model
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tasking.validators import validate_rrule


class TaskLocation(models.Model):
    """
    TaskLocation Model Class
    """
    task = models.ForeignKey(
        'main.Task',
        verbose_name=_('Task'),
        help_text=_('This represents the Task.'),
        on_delete=models.PROTECT
    )
    location = models.ForeignKey(
        'main.Location',
        verbose_name=_('Location'),
        on_delete=models.PROTECT,
        help_text=_('This represents the location')
    )
    timing_rule = models.TextField(
        verbose_name=_('Timing Rule'),
        validators=[validate_rrule],
        help_text=_('This stores the rrule for recurrence.')
    )
    start_time = models.DateTimeField(
        verbose_name=_('Start Time'),
        help_text=_('This is the date and time the task starts.')
    )
    end_time = models.DateTimeField(
        verbose_name=_('End Time'),
        null=True,
        blank=True,
        default=None,
        help_text=_('This is the date and time the task ends.')
    )

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskLocation
        """
        ordering = ['start_time', 'id']
        app_label = 'main'

    def __str__(self):
        """
        Returns string representation for TaskLocation
        """
        return _(f'Task Location for Task: {self.task},'
                 f' Submission: {self.location}')
