"""
Tests for UserProfile serializers
"""
from django.test import TestCase

from kaznet.apps.users.models import UserProfile
from kaznet.apps.users.serializers import UserProfileSerializer


class TestUserProfileSerializer(TestCase):
    """
    Test class for UserProfileSerializer
    """

    def test_create(self):
        """
        Test that you can create a user with the serializer
        """
        data = {
            'first_name': 'Bob',
            'last_name': 'Doe',
            'email': 'bobbie@example.com',
            'gender': UserProfile.MALE,
            'role': UserProfile.ADMIN,
            'expertise': UserProfile.EXPERT,
            'national_id': '123456789',
            'mpesa_number': '+254722222222',
            'phone_number': '+254722222222',
            'ona_pk': 1337,
            'ona_username': 'bobbie'
        }
        # pylint: disable=no-member
        self.assertFalse(
            UserProfile.objects.filter(user__username='bobbie').exists())
        serializer_instance = UserProfileSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        serializer_instance.save()
        self.assertTrue(
            UserProfile.objects.filter(user__username='bobbie').exists())
        self.assertDictContainsSubset(data, serializer_instance.data)
