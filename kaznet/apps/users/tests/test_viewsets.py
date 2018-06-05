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

    def test_list_filtering(self):
        """
        test that you can get and filter a list of userprofiles
        """
        user = create_admin_user()  # ADMIN & EXPERT
        ben = mommy.make('auth.User', first_name='ben')
        ben.userprofile.role = UserProfile.CONTRIBUTOR
        ben.userprofile.expertise = UserProfile.ADVANCED
        ben.userprofile.save()

        alice = mommy.make('auth.User', first_name='alice')
        alice.userprofile.role = UserProfile.CONTRIBUTOR
        alice.userprofile.expertise = UserProfile.ADVANCED
        alice.userprofile.save()

        joe = mommy.make('auth.User', first_name='joe')
        joe.userprofile.role = UserProfile.CONTRIBUTOR
        joe.userprofile.expertise = UserProfile.BEGINNER
        joe.userprofile.save()

        view = UserProfileViewSet.as_view({'get': 'list'})

        request = self.factory.get('/userprofiles')
        force_authenticate(request=request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(4, len(response.data))

        # role filter: there is only one admin
        request2 = self.factory.get(
            '/userprofiles', {'role': UserProfile.ADMIN})
        force_authenticate(request=request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(1, len(response2.data))

        # expertise filter: there are two asvanced users
        request = self.factory.get(
            '/userprofiles', {'expertise': UserProfile.ADVANCED})
        force_authenticate(request=request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.data))

    def test_list_searching(self):
        """
        test that you can get and search a list of userprofiles
        """
        user = create_admin_user()  # ADMIN & EXPERT
        ben = mommy.make('auth.User', first_name='ben')
        ben.userprofile.national_id = 123456
        ben.userprofile.save()

        alice = mommy.make('auth.User', first_name='alice')
        alice.userprofile.national_id = 89768
        alice.userprofile.save()

        joe = mommy.make('auth.User', first_name='joe')
        joe.userprofile.national_id = 1337
        joe.userprofile.save()

        view = UserProfileViewSet.as_view({'get': 'list'})

        # search by national_id
        request = self.factory.get(
            '/userprofiles', {'search': 1337})
        force_authenticate(request=request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data))
        self.assertEqual('joe', response.data[0]['first_name'])

        # search by last name
        request2 = self.factory.get(
            '/userprofiles', {'search': 'alice'})
        force_authenticate(request=request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(1, len(response2.data))
        self.assertEqual('alice', response2.data[0]['first_name'])

    def test_list_ordering(self):
        """
        test that you can get and order a list of userprofiles
        """
        user = create_admin_user()  # ADMIN & EXPERT
        ben = mommy.make('auth.User', first_name='ben')
        mosh = mommy.make('auth.User', first_name='mosh')

        mommy.make('main.Submission', user=ben)
        mommy.make('main.Submission', user=mosh, _quantity=17)

        view = UserProfileViewSet.as_view({'get': 'list'})

        # sort by submission count
        request1 = self.factory.get(
            '/userprofiles', {'ordering': '-submission_count'})
        force_authenticate(request=request1, user=user)
        response1 = view(request=request1)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(3, len(response1.data))
        self.assertEqual('mosh', response1.data[0]['first_name'])
        self.assertEqual('ben', response1.data[1]['first_name'])

        # sort by first_name
        request1 = self.factory.get(
            '/userprofiles', {'ordering': 'first_name'})
        force_authenticate(request=request1, user=user)
        response1 = view(request=request1)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(3, len(response1.data))
        self.assertEqual('ben', response1.data[0]['first_name'])
        self.assertEqual('mosh', response1.data[1]['first_name'])

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
