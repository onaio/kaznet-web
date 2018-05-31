"""
Test for users viewset
"""
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.users.models import UserProfile
from kaznet.apps.users.tests.base import create_admin_user
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
        user = create_admin_user()

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
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(data, response.data)

        return response.data

    def test_create(self):
        """
        Test that you can create userprofiles
        """
        self._create()

    def test_retrieve(self):
        """
        Test that you can retrieve a userprofile object
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        view = UserProfileViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('bob', response.data['first_name'])
        self.assertEqual(bob_userprofile.id, response.data['id'])

    def test_list(self):
        """
        test that you can get a list of userprofiles
        """
        user = create_admin_user()
        mommy.make('auth.User', _quantity=6)

        view = UserProfileViewSet.as_view({'get': 'list'})

        request = self.factory.get('/userprofiles')
        force_authenticate(request=request, user=user)

        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(7, len(response.data))

    def test_update(self):
        """
        Test that you can update userprofiles
        """
        user_data = self._create()
        user = create_admin_user()

        data = {
            'first_name': 'Peter',
            'phone_number': '+254722111111',
            'role': UserProfile.CONTRIBUTOR
        }

        view = UserProfileViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(f'/userprofiles/{user_data["id"]}',
                                     data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=user_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Peter', response.data['first_name'])
        self.assertEqual('+254722111111', response.data['phone_number'])
        self.assertEqual(UserProfile.CONTRIBUTOR, response.data['role'])

    def test_delete(self):
        """
        test that you can delete userprofiles
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        view = UserProfileViewSet.as_view({'delete': 'destroy'})

        request = self.factory.delete(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 204)
        # pylint: disable=no-member
        self.assertFalse(
            UserProfile.objects.filter(id=bob_userprofile.id).exists())
