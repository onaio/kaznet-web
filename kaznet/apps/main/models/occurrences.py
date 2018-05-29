"""
Occurrence models module
"""
from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.translation import ugettext as _

from tasking.models import BaseOccurrence


class TaskOccurrence(BaseOccurrence):
    """
    TaskOccurrence model class
    """
    task = models.ForeignKey(
        'main.Task',
        verbose_name=_('Task Occurrence'),
        on_delete=models.CASCADE
    )

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta for TaskOccurrence
        """
        abstract = False
        ordering = ['task', 'date', 'start_time']

    def __str__(self):
        """
        Returns string representation of the object
        """
        return _(f'{self.task} - {self.get_timestring()}')

    def get_timestring(self):
        """
        Returns a nice human-readable string that represents that date, start
        and end time

        e.g. 24th May 2018, 7 a.m. to 2:30 p.m.
        """

        date = DateFormat(self.date).format('jS F Y')
        start = DateFormat(self.start_time).format('P')
        end = DateFormat(self.end_time).format('P')

        return _(f'{date}, {start} to {end}')
