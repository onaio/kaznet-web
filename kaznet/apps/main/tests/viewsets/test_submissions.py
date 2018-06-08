"""
Tests KaznetSubmissions viewsets.
"""
from datetime import timedelta

from django.utils import timezone

import pytz
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.main.models import Submission
from kaznet.apps.main.viewsets import KaznetSubmissionsViewSet
from kaznet.apps.users.tests.base import create_admin_user
from kaznet.apps.main.tests.base import MainTestBase


class TestKaznetSubmissionViewSet(MainTestBase):
    """
    Test KaznetSubmissionViewSet class
    """

    def setUp(self):
        super(TestKaznetSubmissionViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def test_list_submissions(self):
        """
        Test we are able to list submissions
        """
        user = create_admin_user()
        mommy.make('main.Submission', _quantity=7)
        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        request = self.factory.get('/submissions')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)

    def test_retrieve_submissions(self):
        """
        Test we are able to retrieve a submission
        """
        user = create_admin_user()
        submission = mommy.make('main.Submission')
        view = KaznetSubmissionsViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/submissions/{id}'.format(id=submission.id))

        force_authenticate(request, user=user)

        response = view(request=request, pk=submission.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], submission.id)

    def test_user_filter(self):
        """
        Test able to filter by user
        """
        user = create_admin_user()
        random = mommy.make('auth.User')
        dave = mommy.make('auth.User', username='dave')

        # make a bunch of submissions
        mommy.make('main.Submission', _quantity=7)

        # make one submission using the user mosh
        submission = mommy.make('main.Submission', user=dave)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test that we get submissions for dave
        request = self.factory.get('/submissions', {'user': dave.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)
        self.assertEqual(response.data[0]['user'], dave.id)

        # test dave can filter for his own submissions
        request = self.factory.get('/submissions', {'user': dave.id})
        force_authenticate(request, user=dave)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)
        self.assertEqual(response.data[0]['user'], dave.id)

        # test random users can't filter for daves submissions
        request = self.factory.get('/submissions', {'user': dave.id})
        force_authenticate(request, user=random)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(str(response.data['detail']),
                         'You shall not pass.')

    def test_status_filter(self):
        """
        Test that you can filter by status
        """
        user = create_admin_user()

        # make a bunch of submissions
        mommy.make('main.Submission', status=Submission.PENDING, _quantity=7)

        # make one submission where status is APPROVED
        submission = mommy.make(
            'main.Submission', status=Submission.APPROVED)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test that we get approved submissions
        request = self.factory.get(
            '/submissions', {'status': Submission.APPROVED})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

        # test that we get pending submissions
        request = self.factory.get(
            '/submissions', {'status': Submission.PENDING})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)

    def test_valid_filter(self):
        """
        Test that you can filter by valid
        """
        user = create_admin_user()

        # make a bunch of submissions
        mommy.make('main.Submission', valid=False, _quantity=7)

        # make one submission where valid is True
        submission = mommy.make('main.Submission', valid=True)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test that we get valid submissions
        request = self.factory.get('/submissions', {'valid': 1})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

        # test that we get not valid submissions
        request = self.factory.get('/submissions', {'valid': 0})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)

    def test_location_filter(self):
        """
        Test that you can filter by location
        """
        user = create_admin_user()
        location = mommy.make('main.Location')

        # make a bunch of submissions
        mommy.make('main.Submission', _quantity=7)

        # make one submission using the location
        submission = mommy.make('main.Submission', location=location)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test that we get submissions for our location
        request = self.factory.get('/submissions', {'location': location.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

    def test_task_filter(self):
        """
        Test that you can filter by task
        """
        user = create_admin_user()
        task = mommy.make('main.Task')

        # make a bunch of submissions
        mommy.make('main.Submission', _quantity=7)

        # make one submission using the task
        submission = mommy.make('main.Submission', task=task)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test that we get submissions for our task
        request = self.factory.get('/submissions', {'task': task.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

    def test_submission_time_sorting(self):
        """
        Test that you can sort by submission_time
        """
        now = timezone.now()
        user = create_admin_user()
        # make some submissions
        for i in range(0, 7):
            mommy.make('main.Submission', submission_time=now -
                       timedelta(days=i))

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test sorting
        request = self.factory.get(
            '/submissions', {'ordering': '-submission_time'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        # we have the expected number of records
        self.assertEqual(len(response.data), 7)
        # the first record is what we expect
        # pylint: disable=no-member
        self.assertEqual(
            response.data[0]['id'],
            Submission.objects.order_by('-submission_time').first().id)
        self.assertEqual(
            response.data[0]['submission_time'],
            Submission.objects.order_by(
                '-submission_time').first().submission_time.astimezone(
                    pytz.timezone('Africa/Nairobi')).isoformat())
        # the last record is what we epxect
        self.assertEqual(
            response.data[-1]['id'],
            Submission.objects.order_by('-submission_time').last().id)
        self.assertEqual(
            response.data[-1]['submission_time'],
            Submission.objects.order_by(
                '-submission_time').last().submission_time.astimezone(
                    pytz.timezone('Africa/Nairobi')).isoformat())

    def test_valid_sorting(self):
        """
        Test that you can sort by valid
        """
        user = create_admin_user()

        # make a bunch of submissions
        mommy.make('main.Submission', valid=False, _quantity=7)

        # make one submission where valid is True
        submission = mommy.make('main.Submission', valid=True)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test sorting by valid
        request = self.factory.get('/submissions', {'ordering': 'valid'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(
            response.data[0]['id'],
            Submission.objects.order_by('valid').first().id)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(response.data[-1]['id'], submission.id)

    def test_bounty_amount_sorting(self):
        """
        Test that we can sort by bounty_amount
        """
        user = create_admin_user()
        bounty1 = mommy.make('main.Bounty', amount=400)
        bounty2 = mommy.make('main.Bounty', amount=50)
        bounty3 = mommy.make('main.Bounty', amount=250)

        # make a bunch of submissions
        mommy.make('main.Submission', bounty=bounty3, _quantity=7)

        submission = mommy.make('main.Submission', bounty=bounty1)
        submission1 = mommy.make('main.Submission', bounty=bounty2)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 9)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test sorting in descending order by bounty_amount
        request = self.factory.get(
            '/submissions', {'ordering': '-bounty__amount'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(
            response.data[0]['id'],
            submission.id)
        self.assertEqual(response.data[-1]['id'], submission1.id)

    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        submission = mommy.make('main.Submission')

        # test that you need authentication for retrieving a submission
        view2 = KaznetSubmissionsViewSet.as_view({'get': 'retrieve'})
        request2 = self.factory.get(
            '/submissions/{id}'.format(id=submission.id))
        response2 = view2(request=request2, pk=submission.id)
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response2.data['detail']))

        # test that you need authentication for listing submissions
        view3 = KaznetSubmissionsViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/submissions')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response3.data['detail']))

    def test_permissions_required(self):
        """
        Test Permissions Required when interacting with API Endpoints
        """
        # User cant retrieve submission that isn't theirs

        user = mommy.make('auth.user')
        submission = mommy.make('main.Submission')
        view = KaznetSubmissionsViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/submissions/{id}'.format(id=submission.id))

        force_authenticate(request, user=user)

        response = view(request=request, pk=submission.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(str(response.data['detail']),
                         'You shall not pass.')

        # Can't list all submissions
        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        request = self.factory.get('/submissions')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(str(response.data['detail']),
                         'You shall not pass.')

        # User can retrieve their own submission
        user = mommy.make('auth.User')
        submission = mommy.make('main.Submission', user=user)
        view = KaznetSubmissionsViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get(
            '/submissions/{id}'.format(id=submission.id))

        force_authenticate(request, user=user)

        response = view(request=request, pk=submission.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], submission.id)
        self.assertEqual(response.data['user'], user.id)
