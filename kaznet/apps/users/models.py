# -*- coding: utf-8 -*-
"""
Models module for users app
"""
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from tasking.models.base import TimeStampedModel

from kaznet.apps.users.managers import UserProfileManager

USER = settings.AUTH_USER_MODEL


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

    def __str__(self):
        return _(f"{self.user}'s profile")
