"""

"""

from tasking.models import BaseOccurence

class TaskOccurrence(BaseOccurrence):
    """
    TaskOccurrence model class
    """
    task = models.ForeignKey(
        'tasking.Task',
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
        return '{} - {}'.format(self.task, self.get_timestring())

    def get_timestring(self):
        """
        Returns a nice human-readable string that represents that date, start
        and end time

        e.g. 24th May 2018, 7 a.m. to 2:30 p.m.
        """
        date_format_obj = DateFormat(self.date)
        start_format_obj = DateFormat(self.start_time)
        end_format_obj = DateFormat(self.end_time)

        return '{date}, {start} to {end}'.format(
            date=date_format_obj.format('jS F Y'),
            start=start_format_obj.format('P'),
            end=end_format_obj.format('P')
        )
