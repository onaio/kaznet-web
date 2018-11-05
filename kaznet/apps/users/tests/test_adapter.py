"""
Tests for custom adapters
"""
from unittest.mock import MagicMock

from django.test import RequestFactory

from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.users.adapter import SocialAccountAdapter


class TestSocialAccountAdapter(MainTestBase):
    """
    Test class for SocialAccountAdapter
    """

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_username_already_exists(self):
        """
        Test that we correctly connect the social account to an already
        existing username
        """
        user = mommy.make('auth.User', username='mosh')

        sociallogin = MagicMock()
        sociallogin.connect = MagicMock()
        sociallogin.account.extra_data = {
            'username': 'mosh'
        }
        sociallogin.is_existing = False

        adapter = SocialAccountAdapter()

        request = self.factory.get("/")

        adapter.pre_social_login(request, sociallogin)

        self.assertTrue(sociallogin.connect.called)
        sociallogin.connect.assert_called_with(request, user)

    def test_email_already_exists(self):
        """
        Test that we correctly connect the social account to an already
        existing email
        """
        user = mommy.make('auth.User', email='mosh@example.com')
        mommy.make(
            'account.EmailAddress',
            user=user,
            email='mosh@example.com'
        )

        sociallogin = MagicMock()
        sociallogin.connect = MagicMock()
        sociallogin.account.extra_data = {
            'email': 'mosh@example.com'
        }
        sociallogin.is_existing = False

        adapter = SocialAccountAdapter()

        request = self.factory.get("/")

        adapter.pre_social_login(request, sociallogin)

        self.assertTrue(sociallogin.connect.called)
        sociallogin.connect.assert_called_with(request, user)
