"""
Test for users viewset
"""
from urllib.parse import urljoin

from django.conf import settings
from django.test import override_settings

import requests_mock
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.users.models import UserProfile
from kaznet.apps.users.tests.base import create_admin_user
from kaznet.apps.users.viewsets import UserProfileViewSet
from kaznet.apps.main.models import Submission
from kaznet.apps.users.tests.base import generate_submissions


@override_settings(
    ONA_BASE_URL="https://kaznet.ona.io",
    ONA_ORG_NAME="kaznet",
    ONA_MEMBERS_TEAM_ID=1337,
)
class TestUserProfileViewSet(MainTestBase):
    """
    Test class for UserProfileViewSet
    """

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.ona_json = {
            'id': 1337,
            'metadata': {},
            'gravatar': ""
        }

    def _create(self):
        """
        Helper to create userprofiles with viewset
        """
        with requests_mock.Mocker() as mocked:
            mocked.post(
                urljoin(settings.ONA_BASE_URL, 'api/v1/profiles'),
                status_code=201,
                json=self.ona_json)

            mocked.post(
                urljoin(
                    settings.ONA_BASE_URL,
                    f'api/v1/teams/{settings.ONA_MEMBERS_TEAM_ID}/members'),
                status_code=201)

            mocked.put(
                urljoin(
                    settings.ONA_BASE_URL,
                    f'api/v1/orgs/{settings.ONA_ORG_NAME}/members'),
                status_code=200)

            user = create_admin_user()

            data = {
                'first_name': 'Bob',
                'last_name': 'Doe',
                'email': 'bobbie@example.com',
                'password': 'amalusceaNDb',
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

            # We remove password field since password is write-only
            data.pop('password')

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
        self.assertEqual(7, len(response.data['results']))

    def test_list_filtering(self):
        """
        test that you can get and filter a list of userprofiles
        """
        user = create_admin_user()  # ADMIN & EXPERT
        ben = mommy.make('auth.User', first_name='ben')
        ben.userprofile.role = UserProfile.CONTRIBUTOR
        ben.userprofile.expertise = UserProfile.ADVANCED
        ben.userprofile.ona_username = 'ben'
        ben.userprofile.save()

        alice = mommy.make('auth.User', first_name='alice')
        alice.userprofile.role = UserProfile.CONTRIBUTOR
        alice.userprofile.expertise = UserProfile.ADVANCED
        alice.userprofile.ona_username = 'alice'
        alice.userprofile.save()

        joe = mommy.make('auth.User', first_name='joe')
        joe.userprofile.role = UserProfile.CONTRIBUTOR
        joe.userprofile.expertise = UserProfile.BEGINNER
        joe.userprofile.ona_username = 'joe'
        joe.userprofile.save()

        view = UserProfileViewSet.as_view({'get': 'list'})

        request = self.factory.get('/userprofiles')
        force_authenticate(request=request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(4, len(response.data['results']))

        # role filter: there is only one admin
        request2 = self.factory.get('/userprofiles',
                                    {'role': UserProfile.ADMIN})
        force_authenticate(request=request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(1, len(response2.data['results']))

        # expertise filter: there are two asvanced users
        request = self.factory.get('/userprofiles',
                                   {'expertise': UserProfile.ADVANCED})
        force_authenticate(request=request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.data['results']))

        # ona_username filter: test that we get correct profile
        request = self.factory.get('/userprofiles', {'ona_username': 'joe'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], joe.userprofile.id)

        # test joe can filter for his own profile
        request = self.factory.get('/userprofile', {'ona_username': 'joe'})
        force_authenticate(request, user=joe)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], joe.userprofile.id)

        # test random users can't filter for joes profile
        request = self.factory.get('/submissions', {'ona_username': 'joe'})
        force_authenticate(request, user=alice)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            str(response.data[0]['detail']), 'You shall not pass.')

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
        request = self.factory.get('/userprofiles', {'search': 1337})
        force_authenticate(request=request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data['results']))
        self.assertEqual('joe', response.data['results'][0]['first_name'])

        # search by last name
        request2 = self.factory.get('/userprofiles', {'search': 'alice'})
        force_authenticate(request=request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(1, len(response2.data['results']))
        self.assertEqual('alice', response2.data['results'][0]['first_name'])

    def test_list_ordering(self):
        """
        test that you can get and order a list of userprofiles
        """

        user = create_admin_user()  # ADMIN & EXPERT & First name == 'Ona'
        ben = mommy.make('auth.User', first_name='ben')
        mosh = mommy.make('auth.User', first_name='mosh')
        kyle = mommy.make('auth.User', first_name='kyle')

        mommy.make('main.Submission', user=ben, _quantity=7)
        mommy.make('main.Submission', user=kyle, _quantity=9)
        mommy.make('main.Submission', user=mosh, _quantity=17)

        view = UserProfileViewSet.as_view({'get': 'list'})

        # sort by submission count
        request1 = self.factory.get('/userprofiles',
                                    {'ordering': '-submission_count'})
        force_authenticate(request=request1, user=user)
        response1 = view(request=request1)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual('mosh', response1.data['results'][0]['first_name'])
        self.assertEqual('kyle', response1.data['results'][1]['first_name'])
        self.assertEqual('ben', response1.data['results'][2]['first_name'])

        # sort by first_name
        request1 = self.factory.get('/userprofiles',
                                    {'ordering': 'user__first_name'})
        force_authenticate(request=request1, user=user)
        response1 = view(request=request1)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual('ben', response1.data['results'][0]['first_name'])
        self.assertEqual('kyle', response1.data['results'][1]['first_name'])
        self.assertEqual('mosh', response1.data['results'][2]['first_name'])

    def test_update(self):
        """
        Test that you can update userprofiles
        """
        user_data = self._create()
        user = create_admin_user()

        with requests_mock.Mocker() as mocked:
            mocked.patch(
                urljoin(settings.ONA_BASE_URL,
                        f'api/v1/profiles/{user_data["ona_username"]}'),
                json=self.ona_json,
                status_code=200,
            )

            mocked.put(
                urljoin(
                    settings.ONA_BASE_URL,
                    f'api/v1/orgs/{settings.ONA_ORG_NAME}/members'),
                status_code=200)

            data = {
                'first_name': 'Peter',
                'phone_number': '+254722111111',
                'role': UserProfile.CONTRIBUTOR
            }

            view = UserProfileViewSet.as_view({'patch': 'partial_update'})
            request = self.factory.patch(
                f'/userprofiles/{user_data["id"]}', data=data)
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

    def test_profile(self):
        """
        Test that the profile endpoint returns authenticated
        users profile
        """
        user = create_admin_user()

        view = UserProfileViewSet.as_view({'get': 'profile'})

        request = self.factory.get('/userprofiles/profile')
        force_authenticate(request=request, user=user)

        response = view(request=request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], user.userprofile.id)

    def test_authentication_required(self):
        """
        Test that authentication is required for all endpoints
        """
        # cant create
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
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual('Authentication credentials were not provided.',
                         response.data[0]['detail'])

        user = mommy.make('auth.User')
        userprofile = user.userprofile

        # cant retrieve
        view = UserProfileViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/userprofiles/{userprofile.id}')
        response = view(request=request, pk=userprofile.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual('Authentication credentials were not provided.',
                         response.data[0]['detail'])

        # cant list
        view = UserProfileViewSet.as_view({'get': 'list'})
        request = self.factory.get(f'/userprofiles')
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual('Authentication credentials were not provided.',
                         response.data[0]['detail'])

        # cant update
        data = {
            'first_name': 'Peter',
            'phone_number': '+254722111111',
            'role': UserProfile.CONTRIBUTOR
        }
        view = UserProfileViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            f'/userprofiles/{userprofile.id}', data=data)
        response = view(request=request, pk=userprofile.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual('Authentication credentials were not provided.',
                         response.data[0]['detail'])

        # cant delete
        view = UserProfileViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/userprofiles/{userprofile.id}')
        response = view(request=request, pk=userprofile.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual('Authentication credentials were not provided.',
                         response.data[0]['detail'])

        # cant access profile endpoint
        view = UserProfileViewSet.as_view({'get': 'profile'})
        request = self.factory.get('/userprofiles/profile')
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual('Authentication credentials were not provided.',
                         response.data[0]['detail'])

    def test_permissions_required(self):
        """
        Test that a user must be an Admin to perform any Create, Delete
        or Update request
        """
        # cant create
        with requests_mock.Mocker() as mocked:
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

            mocked_user = mommy.make('auth.User')
            mocked_user2 = mommy.make('auth.User')
            userprofile = mocked_user2.userprofile

            view = UserProfileViewSet.as_view({'post': 'create'})
            request = self.factory.post('/userprofiles', data)
            force_authenticate(request, mocked_user)
            response = view(request=request)
            self.assertEqual(response.status_code, 403)
            self.assertEqual('You shall not pass.', response.data[0]['detail'])

            # cant update userprofile if Requester is not the User linked to it
            data = {
                'first_name': 'Peter',
                'phone_number': '+254722111111',
                'role': UserProfile.CONTRIBUTOR
            }

            mocked.patch(
                urljoin(settings.ONA_BASE_URL,
                        f'api/v1/profiles/{userprofile.user.username}'),
                status_code=200,
                json=self.ona_json
            )

            view = UserProfileViewSet.as_view({'patch': 'partial_update'})
            request = self.factory.patch(
                f'/userprofiles/{userprofile.id}', data=data)
            force_authenticate(request, mocked_user)
            response = view(request=request, pk=userprofile.id)
            self.assertEqual(response.status_code, 403)
            self.assertEqual('You shall not pass.', response.data[0]['detail'])

            # cant delete
            view = UserProfileViewSet.as_view({'delete': 'destroy'})
            request = self.factory.delete(f'/userprofiles/{userprofile.id}')
            force_authenticate(request, mocked_user)
            response = view(request=request, pk=userprofile.id)
            self.assertEqual(response.status_code, 403)
            self.assertEqual('You shall not pass.', response.data[0]['detail'])

            # Cant delete own userprofile
            view = UserProfileViewSet.as_view({'delete': 'destroy'})
            request = self.factory.delete(f'/userprofiles/{userprofile.id}')
            force_authenticate(request, mocked_user2)
            response = view(request=request, pk=userprofile.id)
            self.assertEqual(response.status_code, 403)
            self.assertEqual('You shall not pass.', response.data[0]['detail'])

            # Can update userprofile if Requester is the User linked to it
            data = {
                'first_name': 'Peter',
                'phone_number': '+254722111111',
                'role': UserProfile.CONTRIBUTOR
            }
            view = UserProfileViewSet.as_view({'patch': 'partial_update'})
            request = self.factory.patch(
                f'/userprofiles/{userprofile.id}', data=data)
            force_authenticate(request, mocked_user2)
            response = view(request=request, pk=userprofile.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual('Peter', response.data['first_name'])
            self.assertEqual('+254722111111', response.data['phone_number'])
            self.assertEqual(UserProfile.CONTRIBUTOR, response.data['role'])

    def test_gender_and_gender_display(self):
        """
        Ensure gender and gender dispaly fields are updated correctly
        """
        user_data = self._create()
        user = create_admin_user()

        with requests_mock.Mocker() as mocked:
            mocked.patch(
                urljoin(settings.ONA_BASE_URL,
                        f'api/v1/profiles/{user_data["ona_username"]}'),
                json=self.ona_json,
                status_code=200,
            )

            mocked.put(
                urljoin(
                    settings.ONA_BASE_URL,
                    f'api/v1/orgs/{settings.ONA_ORG_NAME}/members'),
                status_code=200)

            data = {
                'first_name': 'Bob',
                'gender': UserProfile.OTHER,
            }

            view = UserProfileViewSet.as_view({'patch': 'partial_update'})
            request = self.factory.patch(
                f'/userprofiles/{user_data["id"]}', data=data)
            force_authenticate(request, user=user)
            response = view(request=request, pk=user_data['id'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(UserProfile.OTHER, response.data['gender'])
            self.assertEqual("Other", response.data["gender_display"])

            data = {
                'first_name': 'Bob',
                'gender': UserProfile.MALE,
            }

            view = UserProfileViewSet.as_view({'patch': 'partial_update'})
            request = self.factory.patch(
                f'/userprofiles/{user_data["id"]}', data=data)
            force_authenticate(request, user=user)
            response = view(request=request, pk=user_data['id'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(UserProfile.MALE, response.data["gender"])
            self.assertEqual("Male", response.data["gender_display"])

    def test_national_id(self):
        """
        Ensure the national ID field is updated correctly
        """
        user_data = self._create()
        user = create_admin_user()

        with requests_mock.Mocker() as mocked:
            mocked.patch(
                urljoin(settings.ONA_BASE_URL,
                        f'api/v1/profiles/{user_data["ona_username"]}'),
                json=self.ona_json,
                status_code=200,
            )

            mocked.put(
                urljoin(
                    settings.ONA_BASE_URL,
                    f'api/v1/orgs/{settings.ONA_ORG_NAME}/members'),
                status_code=200)

            data = {
                'first_name': 'Bob',
                'national_id': '987654321',

            }

            view = UserProfileViewSet.as_view({'patch': 'partial_update'})
            request = self.factory.patch(
                f'/userprofiles/{user_data["id"]}', data=data)
            force_authenticate(request, user=user)
            response = view(request=request, pk=user_data['id'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual("987654321", response.data['national_id'])

    def test_approved_submissions(self):
        """
        Ensure that a request for approved submmissions returns correct value
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        generate_submissions(
            bob_userprofile, Submission.APPROVED)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bob_userprofile.approved_submissions,
                         response.data['approved_submissions'])

    def test_rejected_submissions(self):
        """
        Ensure that a request for rejected submmissions returns correct value
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        generate_submissions(
            bob_userprofile, Submission.REJECTED)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bob_userprofile.rejected_submissions,
                         response.data['rejected_submissions'])

    def test_avg_amount_earned(self):
        """
        Ensure that a request for rejected submmissions returns correct value
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        generate_submissions(
            bob_userprofile, Submission.APPROVED)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 200)
        space_index = response.data['avg_amount_earned'].index(' ')
        response_avg = response.data['avg_amount_earned'][:space_index]
        self.assertEqual(str(bob_userprofile.avg_amount_earned), response_avg)

    def test_avg_approval_rate(self):
        """
        Ensure that a request for avg_approval_rate returns the correct value
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        generate_submissions(
            bob_userprofile, Submission.APPROVED)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(bob_userprofile.avg_approval_rate),
                         str(response.data["avg_approval_rate"]))

    def test_avg_rejected_submissions(self):
        """
        Ensure that a request for avg_rejected_submissions
        returns the correct value
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        generate_submissions(
            bob_userprofile, Submission.REJECTED)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(bob_userprofile.avg_rejected_submissions), str(
            response.data["avg_rejected_submissions"]))

    def test_avg_approved_submissions(self):
        """
        Ensure that a request for avg_approved_submissions
        returns the correct value
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        generate_submissions(
            bob_userprofile, Submission.APPROVED)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(bob_userprofile.avg_approved_submissions), str(
            response.data["avg_approved_submissions"]))

    def test_avg_submissions(self):
        """
        Ensure that a request for avg_submissions returns the correct value
        """
        user = create_admin_user()
        bob_user = mommy.make('auth.User', first_name='bob')
        bob_userprofile = bob_user.userprofile

        generate_submissions(
            bob_userprofile, Submission.APPROVED)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(f'/userprofiles/{bob_userprofile.id}')
        force_authenticate(request=request, user=user)

        response = view(request=request, pk=bob_userprofile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(bob_userprofile.avg_submissions),
                         str(response.data["avg_submissions"]))
