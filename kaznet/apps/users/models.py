# -*- coding: utf-8 -*-
"""
Models module for users app
"""
from django.conf import settings
from django.db import models
from django.db.models import Value as V
from django.db.models import Avg, Count, Sum
from django.db.models.functions import Coalesce, ExtractMonth
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from tasking.models.base import TimeStampedModel

from kaznet.apps.main.models import Submission
from kaznet.apps.users.managers import UserProfileManager

USER = settings.AUTH_USER_MODEL


# pylint: disable=too-many-public-methods
class UserProfile(TimeStampedModel, models.Model):
    """
    UserProfile model class

    Extends auth.User and adds more fields
    """
    # user roles
    ADMIN = '1'
    CONTRIBUTOR = '2'
    ROLE_CHOICES = (
        (ADMIN, _('Admin')),
        (CONTRIBUTOR, _('Contributor'))
    )

    # user expertise
    BEGINNER = '1'
    INTERMEDIATE = '2'
    ADVANCED = '3'
    EXPERT = '4'
    EXPERTISE_CHOICES = (
        (BEGINNER, _('Beginner')),
        (INTERMEDIATE, _('Intermediate')),
        (ADVANCED, _('Advanced')),
        (EXPERT, _('Expert'))
    )

    # gender
    OTHER = '0'
    MALE = '1'
    FEMALE = '2'
    GENDER_CHOICES = (
        (OTHER, _('Other')),
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )

    user = models.OneToOneField(
        USER, verbose_name=_('User'), on_delete=models.CASCADE)
    ona_pk = models.PositiveIntegerField(
        _('Ona Primary key'), db_index=True, unique=True, null=True,
        default=None, blank=True)
    ona_username = models.CharField(
        _('Ona Username'), db_index=True, unique=True, null=True, default=None,
        blank=True, max_length=255)
    national_id = models.CharField(
        _('National ID Number'), db_index=True, unique=True, null=True,
        default=None, blank=True, max_length=255)
    payment_number = PhoneNumberField(
        _('Payment phone number'), blank=True, default='',
        help_text=_('Mobile money payment phone nerumber'))
    phone_number = PhoneNumberField(_('Phone number'), blank=True, default='')
    role = models.CharField(_('Role'), choices=ROLE_CHOICES,
                            default=CONTRIBUTOR, max_length=1, blank=True)
    expertise = models.CharField(_('Expertise'), choices=EXPERTISE_CHOICES,
                                 default=BEGINNER, max_length=1, blank=True)
    gender = models.CharField(
        _('Gender'), max_length=1, choices=GENDER_CHOICES, default=OTHER,
        blank=True)

    # custom manager
    objects = UserProfileManager()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta Options for UserProfile
        """
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ['user__first_name', 'user__last_name', 'user__email']

    # pylint: disable=no-member
    def get_name(self):
        """
        Get pretty name for this user profile
        """
        if self.user.get_full_name():
            return self.user.get_full_name()
        if self.user.email:
            return self.user.email
        return self.user.username

    def __str__(self):
        return f"{self.get_name()}'s profile"

    # pylint: disable=no-member
    def get_approved_submissions(self):
        """
        Returns the number of approved submission for user
        """
        return self.user.submission_set.filter(
            status=Submission.APPROVED).count()

    def get_rejected_submissions(self):
        """
        Returns the number of approved submission for user
        """
        return self.user.submission_set.filter(
            status=Submission.REJECTED).count()

    def get_approval_rate(self):
        """
        Returns the approval rate for user
        """
        approved = self.user.submission_set.filter(
            status=Submission.APPROVED).count()
        all_submissions = self.user.submission_set.all().count()
        if all_submissions > 0:
            return approved / all_submissions
        return 0.0

    def get_avg_submissions(self):
        """
        Gets Average Submissions per month for user
        """
        return self.user.submission_set.annotate(
            month_sub=ExtractMonth('submission_time')
            ).values('month_sub').annotate(
                count=Count('month_sub')
                ).order_by().aggregate(submissions=Coalesce(
                    Avg('count'), V(0)))

    def get_avg_approved_submissions(self):
        """
        Gets Average Approved Submissions per month for
        User
        """
        return self.user.submission_set.filter(
            status=Submission.APPROVED).annotate(
                month_sub=ExtractMonth('submission_time')
                ).values('month_sub').annotate(
                    count=Count('month_sub')
                    ).order_by().aggregate(submissions=Coalesce(
                        Avg('count'), V(0)))

    def get_avg_rejected_submissions(self):
        """
        Gets Rejected Approved Submissions per month for
        User
        """
        return self.user.submission_set.filter(
            status=Submission.REJECTED).annotate(
                month_sub=ExtractMonth('submission_time')
                ).values('month_sub').annotate(
                    count=Count('month_sub')
                    ).order_by().aggregate(submissions=Coalesce(
                        Avg('count'), V(0)))

    def get_avg_approval_rate(self):
        """
        Gets Average Approval Rate for User
        """
        avg_submissions = self.avg_submissions
        avg_approved_submissions = self.avg_approved_submissions
        if avg_submissions > 0:
            return avg_approved_submissions / avg_submissions
        return 0.0

    def get_amount_earned(self):
        """
        Returns the amount earned by user
        """
        return self.user.submission_set.filter(
            status=Submission.APPROVED).aggregate(amount=Coalesce(
                Sum('bounty__amount'), V(0)))

    def get_avg_amount_earned(self):
        """
        Returns Average Amount Earned Per Month
        """
        return self.user.submission_set.filter(
            status=Submission.APPROVED).annotate(
                month_sub=ExtractMonth('submission_time')
                ).values('month_sub').annotate(
                    amount_earned=Sum('bounty__amount')
                    ).order_by().aggregate(amount=Coalesce(
                        Avg('amount_earned'), V(0)))

    @property
    def approved_submissions(self):
        """
        Returns the number of approved submissions for user
        """
        return self.get_approved_submissions()

    @property
    def rejected_submissions(self):
        """
        Returns the number of rejected submissions for user
        """
        return self.get_rejected_submissions()

    @property
    def role_display(self):
        """
        Returns Role in a Human Readable Format
        """
        return self.get_role_display()

    @property
    def expertise_display(self):
        """
        Returns the Expertise Level in a Human Readable Format
        """
        return self.get_expertise_display()

    @property
    def gender_display(self):
        """
        Returns Gender in a Human Readable Format
        """
        return self.get_gender_display()

    @property
    def approval_rate(self):
        """
        Returns the users approval rate
        """
        return self.get_approval_rate()

    @property
    def amount_earned(self):
        """
        Total amount earned
        """
        return self.get_amount_earned()['amount']

    @property
    def avg_submissions(self):
        """
        Returns the Average Submissions Per Month
        for User
        """
        return self.get_avg_submissions()['submissions']

    @property
    def avg_approved_submissions(self):
        """
        Returns the Average Approved Submissions Per Month
        for User
        """
        return self.get_avg_approved_submissions()['submissions']

    @property
    def avg_rejected_submissions(self):
        """
        Returns the Average Approved Submissions Per Month
        for User
        """
        return self.get_avg_rejected_submissions()['submissions']

    @property
    def avg_approval_rate(self):
        """
        Returns the Average Approval Rate For User
        """
        return self.get_avg_approval_rate()

    @property
    def avg_amount_earned(self):
        """
        Returns the Average Amount Earned Per Month
        """
        return self.get_avg_amount_earned()['amount']
