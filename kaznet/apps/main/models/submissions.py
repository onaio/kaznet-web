"""
Module for the Task Submission model(s)
"""
from django.db import models
from django.utils.translation import ugettext as _

from tasking.models import BaseSubmission
from kaznet.apps.main.models.managers import SubmissionManager


class Submission(BaseSubmission):
    """
    Submission model class
    """
    task = models.ForeignKey(
        'main.Task',
        verbose_name=_('Task'),
        on_delete=models.PROTECT,
        help_text=_('This represents the Task.')
    )
    bounty = models.ForeignKey(
        'main.Bounty',
        verbose_name=_('Bounty'),
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('This represents the Bounty.')
    )
    location = models.ForeignKey(
        'main.Location',
        verbose_name=_('Location'),
        blank=True,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        help_text=_('This represents the Location.')
    )
    objects = SubmissionManager()

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        This is the meta options class for the Submission model
        """
        abstract = False
        ordering = ['submission_time', 'task__name', 'id']
        app_label = 'main'

    def __str__(self):
        """
        String representation of a Submission object

        e.g. Cattle Price - 1 submission 1
        """
        return _(f"{self.task} submission {self.pk}")

    def get_approved(self, status):
        """
        Class method that gets the value of approved property
        """
        if status == self.APPROVED:
            return True
        if status == self.REJECTED:
            return False

        return None

    @property
    def approved(self):
        """
        Approved class property for submission
        """
        return self.get_approved(self.status)

    @property
    def amount(self):
        """
        Get the bounty amount
        """
        if self.bounty:
            return self.bounty.amount  # pylint: disable=no-member
        return None
