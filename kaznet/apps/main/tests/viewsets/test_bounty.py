"""
Tests module for BountyViewSet
"""

from collections import OrderedDict

from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.main.models import Bounty
from kaznet.apps.main.serializers import BountySerializer
from kaznet.apps.main.viewsets import BountyViewSet
from kaznet.apps.users.tests.base import create_admin_user


class TestBountyViewSet(TestCase):
    """
    Test for ClientViewSet
    """

    def setUp(self):
        super(TestBountyViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_bounty(self):
        """
        Helper method to create bounty
        """

        task = mommy.make('main.Task', name='Ep1c')
        task_data = OrderedDict(
            type='Task',
            # Needs to be a string so as to not cause a conflict on
            # Dict assertation after serialization
            id=f'{task.id}'
        )

        data = {
            "task": task_data,
            "amount": '5400.00'
        }

        serializer_instance = BountySerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        serializer_instance.save()

        return serializer_instance.data

    def test_retrieve_bounty(self):
        """
        Test GET /bounty/[pk] return a bounty matching pk.
        """
        user = create_admin_user()
        bounty_data = self._create_bounty()

        view = BountyViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/bounty/{id}'.format(id=bounty_data['id']))
        force_authenticate(request, user=user)
        response = view(request=request, pk=bounty_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, bounty_data)

    def test_list_bounty(self):
        """
        Test GET /bounty listing of bounty for specific forms.
        """
        user = create_admin_user()
        bounty_data = self._create_bounty()
        view = BountyViewSet.as_view({'get': 'list'})

        request = self.factory.get('/bounty')
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data['results'].pop(), bounty_data)

    def test_task_filter(self):
        """
        Test Task Filter
        """
        user = create_admin_user()
        task = mommy.make('main.Task')

        # make a bunch of bounties
        mommy.make('main.Bounty', _quantity=7)

        # make one bounty using the task
        bounty = mommy.make('main.Bounty', task=task)

        # check that we have 8 bounties
        # pylint: disable=no-member
        self.assertEqual(Bounty.objects.all().count(), 8)

        view = BountyViewSet.as_view({'get': 'list'})

        # test that we get bounty for our task
        request = self.factory.get('/bounty', {'task_id': task.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], bounty.id)

    def test_submission_filter(self):
        """
        Test Submission_id filter
        """
        user = create_admin_user()
        task = mommy.make('main.Task')

        mommy.make('main.Bounty', _quantity=7)
        bounty = mommy.make('main.Bounty', task=task)

        # Make a submission for the bounty
        submission = mommy.make('main.Submission', bounty=bounty)

        # check that we have 8 bounties
        # pylint: disable=no-member
        self.assertEqual(Bounty.objects.all().count(), 8)

        view = BountyViewSet.as_view({'get': 'list'})

        # test that we get bounty for our task
        request = self.factory.get('/bounty', {'submission': submission.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], bounty.id)

    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        bounty_data = self._create_bounty()

        view = BountyViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/bounty/{id}'.format(id=bounty_data['id']))
        response = view(request=request, pk=bounty_data['id'])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data[0]['detail']))

        view = BountyViewSet.as_view({'get': 'list'})

        request = self.factory.get('/bounty')
        response = view(request=request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data[0]['detail']))
