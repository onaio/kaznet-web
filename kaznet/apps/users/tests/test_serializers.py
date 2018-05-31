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

    def _create_user(self):
        """
        Utility to create users
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

        return serializer_instance.data

    def test_create(self):
        """
        Test that you can create a user with the serializer
        """
        serializer_instance = self._create_user()

        fields = [
            'id',
            'created',
            'modified',
            'first_name',
            'last_name',
            'email',
            'ona_pk',
            'ona_username',
            'mpesa_number',
            'phone_number',
            'role',
            'expertise',
            'gender',
            'national_id'
        ]

        self.assertEqual(set(fields), set(serializer_instance.keys()))

    def test_update(self):
        """
        Test that you cna update a suer with the serializer
        """
        initial_user_data = self._create_user()

        data = {
            'first_name': 'Mosh',
            'last_name': 'Pitt',
            'email': 'mosh@example.com',
            'role': UserProfile.CONTRIBUTOR,
            'expertise': UserProfile.INTERMEDIATE,
            'national_id': '1337',
            'mpesa_number': '+254722111111',
            'ona_pk': 9999,
            'ona_username': 'mosh'
        }

        # pylint: disable=no-member
        userprofile = UserProfile.objects.get(user__username='bobbie')
        serializer_instance = UserProfileSerializer(
            instance=userprofile,
            data=data)
        self.assertTrue(serializer_instance.is_valid())
        serializer_instance.save()

        expected_data = dict(initial_user_data).copy()
        expected_data['first_name'] = 'Mosh'
        expected_data['last_name'] = 'Pitt'
        expected_data['email'] = 'mosh@example.com'
        expected_data['role'] = UserProfile.CONTRIBUTOR
        expected_data['expertise'] = UserProfile.INTERMEDIATE
        expected_data['national_id'] = '1337'
        expected_data['mpesa_number'] = '+254722111111'

        self.assertDictContainsSubset(expected_data, serializer_instance.data)

        userprofile.refresh_from_db()

        self.assertEqual('Mosh', userprofile.user.first_name)
        self.assertEqual('Pitt', userprofile.user.last_name)
        self.assertEqual('mosh@example.com', userprofile.user.email)
        self.assertEqual(UserProfile.CONTRIBUTOR, userprofile.role)
        self.assertEqual(UserProfile.INTERMEDIATE, userprofile.expertise)
        self.assertEqual('1337', userprofile.national_id)
        self.assertEqual('+254722111111', userprofile.mpesa_number.as_e164)
