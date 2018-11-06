"""
Test for UserProfile model
"""
from model_mommy import mommy
from rest_framework.authtoken.models import Token

from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.users.models import UserProfile


class TestUserModels(MainTestBase):
    """
    Test class for User models
    """

    def setUp(self):
        super().setUp()

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

    def test_create_auth_token(self):
        """
        Test that auth token is created when user is created
        """
        user = mommy.make('auth.User', username='mosh')
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_submission_count(self):
        """
        Test that submission_count works
        """
        userprofile = mommy.make('auth.User').userprofile
        # make some submissions
        mommy.make('main.Submission', _quantity=789, user=userprofile.user)

        # user .objects so that we can get the submission count
        profile = UserProfile.objects.get(id=userprofile.id)

        self.assertEqual(789, profile.submission_count)
