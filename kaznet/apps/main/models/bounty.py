"""
Module for the Bounty model(s)
"""
from django.db import models
from django.utils.translation import ugettext as _

from django_prices.models import MoneyField
from tasking.models.base import TimeStampedModel

from django.conf import settings


class Bounty(TimeStampedModel):
    """
    Bounty model class
    """
    modified = None

    task = models.ForeignKey(
        'main.Task',
        verbose_name=_('Task'),
        on_delete=models.CASCADE,
        help_text=_('The task the bounty is for.'),
    )

    amount = MoneyField(
        verbose_name=_('Amount'),
        decimal_places=2,
        max_digits=64,
        default=0,
        currency=settings.KAZNET_DEFAULT_CURRENCY
    )

    def __str__(self):
        """
        String representation of a Task object

        e.g. Task 1 bounty is 5000
        """
        # pylint: disable=no-member
        return _(f"Task {self.task.id} bounty is {self.amount}")

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the Bounty Model
        """
        ordering = ['created', 'id']
        abstract = False
