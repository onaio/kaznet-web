# -*- coding: utf-8 -*-
"""
Models module for users app
"""
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

USER = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    """
    UserProfile model class

    Extends auth.User and adds more fields
    """
    user = models.OneToOneField(
        USER, verbose_name=_("User"), on_delete=models.CASCADE)

    def __str__(self):
        return _(f"{self.user}'s profile")
