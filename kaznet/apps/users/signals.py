# -*- coding: utf-8 -*-
"""
Signals module for user app
"""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from kaznet.apps.users.models import UserProfile

USER = settings.AUTH_USER_MODEL


@receiver(post_save, sender=USER)
# pylint: disable=unused-argument
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create UserProfile model when a new User model is created
    """
    if created or not instance.userprofile:
        # pylint: disable=no-member
        UserProfile.objects.get_or_create(user=instance)
