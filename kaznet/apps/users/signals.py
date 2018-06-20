# -*- coding: utf-8 -*-
"""
Signals module for user app
"""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
# pylint: disable=unused-argument
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create auth tokens when a user is created
    """
    if created:
        Token.objects.create(user=instance)  # pylint: disable=no-member
