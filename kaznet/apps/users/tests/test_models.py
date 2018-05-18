# -*- coding: utf-8 -*-
"""
Test for Location model
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from kaznet.apps.users.models import UserProfile


class TestUserModels(TestCase):
    """
    Test class for User models
    """

    def test_userprofile_model_creation(self):
        """
        Test that a UserProfile model is created when a User is created
        """
        user = mommy.make('auth.User', username='mosh')
        # assert that we have a userprofile object attached
        self.assertTrue(isinstance(user.userprofile, UserProfile))
        # check the username
        self.assertEqual('mosh', user.userprofile.user.username)
        # check the __str__ method on UserProfile
        self.assertEqual("mosh's profile", user.userprofile.__str__())
