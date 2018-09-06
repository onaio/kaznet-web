"""
Test users app signals
"""
from django.test import TestCase

from model_mommy import mommy


class TestSignals(TestCase):
    """
    Tests for Kanzet app signals
    """

    def test_sync_onadata_oauth_profile(self):
        """
        Test sync_onadata_oauth_profile
        """
        user = mommy.make('auth.User', username='mosh')
        userprofile = user.userprofile

        # clear ona_username and gravatar
        userprofile.metadata = dict()
        userprofile.ona_username = None
        userprofile.save()

        # create a socialaccount object for this user
        extra_data = {
            "url": "https://example.com",
            "username": "mosh",
            "name": "Mosh",
            "email": "mosh@example.com",
            "city": "",
            "country": "",
            "organization": "",
            "website": "",
            "twitter": "",
            "gravatar": "https://example.com/gravatar_url",
            "require_auth": True,
            "user": "https://example.com/mosh",
            "api_token": "api token",
            "temp_token": "temp token"
        }
        mommy.make(
            'socialaccount.SocialAccount',
            user=user,
            provider='onadata',
            uid='mosh',
            extra_data=extra_data
        )

        # check that the profile was updated when the post_save signal sent
        userprofile.refresh_from_db()
        self.assertEqual('mosh', userprofile.ona_username)
        self.assertEqual(
            'https://example.com/gravatar_url',
            userprofile.metadata.get('gravatar')
        )
