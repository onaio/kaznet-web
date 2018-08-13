"""
Authentication Tests Module
"""

from unittest.mock import patch
from urllib.parse import urljoin

from django.conf import settings
from django.test import TestCase, override_settings

import requests_mock
from model_mommy import mommy
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.main.common_tags import (AUTH_USER_DOESNT_EXIST,
                                          AUTH_USER_NOT_LOGGED_IN)


class TestOnaTempTokenAuthentication(TestCase):
    """
    Tests OnaTempTokenAuthentication
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mommy.make(
            'auth.User',
            username='Davis',
        )

        # Set ona_username on profile
        self.user_profile = self.user.userprofile
        self.user_profile.ona_username = 'dave'
        self.user_profile.save()

        self.ona_response = {
            'username': 'dave',
            'name': 'Dave',
            'email': 'dave@tester.test',
        }
        self.auth = OnaTempTokenAuthentication()

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
    @requests_mock.Mocker()
    def test_authenticates_credentials(self, mocked):
        """
        Test:
            - Authenticates user if User Exists
              and is Logged in to Ona
            - Doesn't authenticate user if User Doesn't exist
              even if Logged into Ona
            - Doesn't authenticate user if user isn't logged into
              ona
        """

        # Test it authenticates if Ona User is Logged In
        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/user'),
            json=self.ona_response,
            )

        returned_user = self.auth.authenticate_credentials(
            'token'
        )[0]

        self.assertEqual(self.user, returned_user)

        # Test it doesn't authenticate  if User doesn't exist
        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/user'),
            json={
                'username': 'intruder'
                }
            )

        self.assertRaisesMessage(
            AuthenticationFailed,
            f'{AUTH_USER_DOESNT_EXIST}',
            self.auth.authenticate_credentials,
            'token'
        )

        # Test it doesn't authenticate if User isn't logged onto Ona
        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/user'),
            status_code=401
            )

        self.assertRaisesMessage(
            AuthenticationFailed,
            f'{AUTH_USER_NOT_LOGGED_IN}',
            self.auth.authenticate_credentials,
            'token'
        )

    @override_settings(
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }
        )
    @patch('django.core.cache.cache.set')
    @requests_mock.Mocker()
    def test_authenticate_credentials_caches(
            self, mockedSet, mocked):
        """
        Test:
            - Caches a Users Profile after authentication
        """

        # Test Caches User Profile
        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/user'),
            json=self.ona_response,
            )

        self.auth.authenticate_credentials(
            'token'
        )

        mockedSet.assert_called_with(
            'token', self.user_profile.ona_username, 14400)

    @patch('kaznet.apps.ona.api.request_session')
    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_authenticate_credentials_reads_cache(
            self, mockedSet, mockedGet, mockedRequest):
        """
        Test:
            - Doesn't authenticate with Ona if User is already
              cached
            - Doesn't cache if authentication is already cached
        """

        mockedGet.return_value = self.user_profile.ona_username

        self.auth.authenticate_credentials(
            'token'
        )

        self.assertFalse(mockedSet.called)
        self.assertFalse(mockedRequest.called)
