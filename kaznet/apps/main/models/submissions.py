"""

"""

from tasking.models import BaseSubmission


class Submission(BaseSubmission):
    """
    Submission model class
    """
    task = models.ForeignKey(
        'tasking.Task',
        verbose_name=_('Task'),
        on_delete=models.PROTECT,
        help_text=_('This represents the Task.')
    )
    location = models.ForeignKey(
        'tasking.Location',
        verbose_name=_('Location'),
        blank=True,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        help_text=_('This represents the Location.')
    )

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the Submission model
        """
        abstract = False
        ordering = ['submission_time', 'task__name', 'id']

    def __str__(self):
        """
        String representation of a Submission object

        e.g. Cattle Price - 1 submission 1
        """
        return "{task} submission {submission_id}".format(
            submission_id=self.pk, task=self.task)

    def get_approved(self, status):
        """
        Class method that gets the value of approved property
        """
        if status == self.APPROVED:
            return True
        elif status == self.REJECTED:
            return False

        return None

    @property
    def approved(self):
        """
        Approved class property for submission
        """
        return self.get_approved(self.status)
