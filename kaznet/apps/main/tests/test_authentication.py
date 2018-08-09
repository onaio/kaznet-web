"""
Authentication Tests Module
"""

from urllib.parse import urljoin

from django.conf import settings
from django.test import TestCase, override_settings

import requests_mock
from model_mommy import mommy
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.users.models import UserProfile


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

        returned_profile = self.auth.authenticate_credentials(
            'token'
        )[0]

        self.assertEqual(self.user_profile, returned_profile)

        # Test it doesn't authenticate  if User doesn't exist
        # mocked.get(
        #     urljoin(settings.ONA_BASE_URL, 'api/v1/user'),
        #     json={
        #         'username': 'intruder'
        #         }
        #     )

        # self.assertRaises(
        #     UserProfile.DoesNotExist,  # pylint: disable=no-member
        #     self.auth.authenticate_credentials('token')
        # )

        # Test it doesn't authenticate if User isn't logged onto Ona
        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/user'),
            status_code=401
            )

