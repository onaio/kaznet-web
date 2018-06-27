"""
Module for the Task model(s)
"""
from django.db import models
from django.db.models import Value as V
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext as _

from tasking.models import BaseTask

from kaznet.apps.main.models.managers import TaskManager


class Task(BaseTask):
    """
    Task model class
    """

    BEGINNER = '1'
    INTERMEDIATE = '2'
    ADVANCED = '3'
    EXPERT = '4'

    EXPERTISE_CHOICES = (
        (BEGINNER, _('Beginner')),
        (INTERMEDIATE, _('Intermediate')),
        (ADVANCED, _('Advanced')),
        (EXPERT, _('Expert')),
    )

    segment_rules = models.ManyToManyField(
        'main.SegmentRule',
        verbose_name=_('Segment Rules'),
        blank=True,
        default=None
    )
    locations = models.ManyToManyField(
        'main.Location',
        verbose_name=_('Location'),
        blank=True,
        default=None,
        help_text=_('This represents the location.'))
    client = models.ForeignKey(
        'main.Client',
        verbose_name=_('Client'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        help_text=_('This represents the client.')
    )
    required_expertise = models.CharField(
        _('Recommended Expertise'),
        choices=EXPERTISE_CHOICES,
        default=BEGINNER,
        max_length=1,
        blank=True)

    # Custom Manager that has submission_count field
    with_submission_count = TaskManager()

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the Task model
        """
        abstract = False
        unique_together = ('target_content_type', 'target_object_id')
        ordering = ['start', 'name', 'id']
        app_label = 'main'

    def __str__(self):
        """
        String representation of a Task object

        e.g. Cow prices - 1
        """
        return _(f"{self.name} - {self.pk}")

    # pylint: disable=no-member
    def get_submissions(self):
        """
        Custom method to get number of submissions
        """
        return self.submission_set.count()

    def get_approved_submissions(self):
        """
        Custom method to get number of accepted submissions
        """
        return self.submission_set.filter(status='a').count()

    def get_pending_submissions(self):
        """
        Custom method to get number of pending submissions
        """
        return self.submission_set.filter(status='d').count()

    def get_rejected_submissions(self):
        """
        Custom method to get number of rejected submissions
        """
        return self.submission_set.filter(status='b').count()

    def get_total_bounty_payout(self):
        """
        Custom method to get total bounty amount for all
        approved submissions
        """
        return self.submission_set.filter(status='a').aggregate(
            combined_amount=Coalesce(
                Sum('bounty__amount'), V(0)))

    def get_bounty(self):
        """
        Custom method to get latest bounty for task
        """
        return self.bounty_set.all().order_by('-created').first()

    def get_xform_title(self):
        """
        Custom Method to get xform title
        """
        try:
            return self.target_content_object.title
        except AttributeError:
            return ''

    @property
    def status_display(self):
        """
        Human Readable Status
        """
        return self.get_status_display()

    @property
    def xform_title(self):
        """
        Title of Xform
        """
        return self.get_xform_title()

    @property
    def required_expertise_display(self):
        """
        Human Readable Required Expertise
        """
        return self.get_required_expertise_display()

    @property
    def submissions(self):
        """
        Number of Submissions made for this task
        """
        return self.get_submissions()

    @property
    def approved_submissions_count(self):
        """
        Number of Approved Submissions
        """
        return self.get_approved_submissions()

    @property
    def pending_submissions_count(self):
        """
        Number of Pending Submissions
        """
        return self.get_pending_submissions()

    @property
    def rejected_submissions_count(self):
        """
        Number of Rejected Submissions
        """
        return self.get_rejected_submissions()

    @property
    def bounty(self):
        """
        Latest bounty for Task
        """
        return self.get_bounty()

    @property
    def current_bounty_amount(self):
        """
        Get the current bounty amount
        """
        bounty = self.get_bounty()
        if bounty is not None:
            return bounty.amount
        return None

    @property
    def total_bounty_payout(self):
        """
        Total Amount to be paid for Task Submissions
        """
        return self.get_total_bounty_payout()['combined_amount']
