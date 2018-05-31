"""
Test for users viewset
"""
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.users.models import UserProfile
from kaznet.apps.users.viewsets import UserProfileViewSet


class TestUserProfileViewSet(TestCase):
    """
    Test class for UserProfileViewSet
    """

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()

    def _create(self):
        """
        Helper to create userprofiles with viewset
        """
        user = mommy.make('auth.User')
        data = {
            'first_name': 'Bob',
            'last_name': 'Doe',
            'email': 'bobbie@example.com',
            'gender': UserProfile.MALE,
            'role': UserProfile.ADMIN,
            'expertise': UserProfile.EXPERT,
            'national_id': '123456789',
            'payment_number': '+254722222222',
            'phone_number': '+254722222222',
            'ona_pk': 1337,
            'ona_username': 'bobbie'
        }

        view = UserProfileViewSet.as_view({'post': 'create'})
        request = self.factory.post('/userprofiles', data)
        # need to authenticate
        force_authenticate(request, user=user)
        response = view(request=request)

        # assert that we get the right status_code and data back
        self.assertEqual(response.status_code, 201, response.data)
        self.assertDictContainsSubset(data, response.data)

        return response.data

    def test_create(self):
        """
        Test that you can create userprofiles
        """
        self._create()
