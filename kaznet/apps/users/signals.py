# -*- coding: utf-8 -*-
"""
Signals module for user app
"""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount
from allauth_onadata.provider import OnadataAccount
from rest_framework.authtoken.models import Token

from kaznet.apps.users.models import UserProfile

USER = settings.AUTH_USER_MODEL


@receiver(
    post_save, sender=USER, dispatch_uid='create_user_profile')
# pylint: disable=unused-argument
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create UserProfile model when a new User model is created
    """
    if created or not instance.userprofile:
        # pylint: disable=no-member
        UserProfile.objects.get_or_create(user=instance)


@receiver(
    post_save, sender=settings.AUTH_USER_MODEL,
    dispatch_uid='create_auth_token')
# pylint: disable=unused-argument
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create auth tokens when a user is created
    """
    if created:
        Token.objects.create(user=instance)  # pylint: disable=no-member


@receiver(
    post_save, sender=SocialAccount,
    dispatch_uid='sync_onadata_oauth_profile')
# pylint: disable=unused-argument
def sync_onadata_oauth_profile(sender, instance=None, created=False, **kwargs):
    """
    The SocialAccount model holds user information received from Oauth
    providers.  Here, we attempt to sync this information with our local
    UserProfile model.
    """
    oauth_provider = instance.get_provider()
    # check if the Oauth provider is Onadata
    if oauth_provider and oauth_provider.account_class == OnadataAccount:
        try:
            # get the local userprofile
            userprofile = instance.user.userprofile
        except UserProfile.DoesNotExist:  # pylint: disable=no-member
            pass
        else:
            # get the fields we want
            gravatar_url = instance.extra_data.get('gravatar')
            ona_username = instance.extra_data.get('username')
            # save/update the fields we are interested in
            if ona_username:
                userprofile.ona_username = ona_username
            if gravatar_url:
                userprofile.metadata['gravatar'] = gravatar_url
            if any([gravatar_url, ona_username]):
                userprofile.save()
