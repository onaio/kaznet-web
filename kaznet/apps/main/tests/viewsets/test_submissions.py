"""
Tests KaznetSubmissions viewsets.
"""
from datetime import timedelta
from io import BytesIO

from django.utils import timezone

import pytz
from dateutil.parser import parse
from django_prices.models import Money
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.main.models import Submission, Task, Location
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.main.viewsets import (KaznetSubmissionsViewSet,
                                       SubmissionExportViewSet)
from kaznet.apps.users.tests.base import create_admin_user


class TestSubmissionExportViewSet(MainTestBase):
    """
    Test SubmissionExportViewSet
    """

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.expected = b"id,user,user_id,task,task_id,location,location_id,submission_time,approved,status,comments,amount,currency,phone_number,payment_number\r\n888,Coco,1377,Quest,2001,Voi,1000,2018-09-04T00:00:00+00:00,True,a,,50.00,KES,,\r\n999,Coco,1377,Quest,2001,Voi,1000,2018-09-04T00:00:00+00:00,True,a,,50.00,KES,,\r\n"  # noqa
        # make two submissions that work with self.expected
        try:
            self.task = Task.objects.get(id=2001)
        except Task.DoesNotExist:

            task = mommy.make('main.Task', name='Quest')
            task.id = 2001
            task.save(force_insert=True)
            self.task = task

        try:
            self.location = Location.objects.get(id=1000)
        except Location.DoesNotExist:

            location = mommy.make('main.Location', name='Voi')
            location.id = 1000
            location.save(force_insert=True)
            self.location = location

        self.coco_user = mommy.make('auth.User', first_name='Coco', id=1377)
        mommy.make(
            'main.Submission',
            task=self.task,
            location=self.location,
            user=self.coco_user,
            bounty=mommy.make(
                'main.Bounty',
                task=self.task,
                amount=Money('50', 'KES')),
            submission_time=parse("2018-09-04T00:00:00+00:00"),
            status=Submission.APPROVED,
            id=888
        )
        mommy.make(
            'main.Submission',
            task=self.task,
            location=self.location,
            user=self.coco_user,
            bounty=mommy.make(
                'main.Bounty',
                task=self.task,
                amount=Money('50', 'KES')),
            submission_time=parse("2018-09-04T00:00:00+00:00"),
            status=Submission.APPROVED,
            id=999
        )

    def test_csv_export(self):
        """
        Test CSV export
        """
        user = create_admin_user()

        view = SubmissionExportViewSet.as_view({'get': 'list'})

        request = self.factory.get('/exports/submissions', {'format': 'csv'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)

        received = BytesIO(b''.join(response.streaming_content)).getvalue()

        self.assertEqual(self.expected, received)

    def test_csv_export_task_filter(self):
        """
        Test CSV export task filter
        """
        user = create_admin_user()

        # make 3 other random submissions
        mommy.make('main.Submission', _quantity=3)

        view = SubmissionExportViewSet.as_view({'get': 'list'})

        request = self.factory.get(
            '/exports/submissions',
            {'format': 'csv', 'task': self.task.id}
        )
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)

        received = BytesIO(b''.join(response.streaming_content)).getvalue()

        # we have filtered out the 3 new submissions, check our data
        self.assertEqual(self.expected, received)

    def test_csv_export_user_filter(self):
        """
        Test CSV export user filter
        """
        user = create_admin_user()

        # make 16 other random submissions
        mommy.make('main.Submission', _quantity=16)

        view = SubmissionExportViewSet.as_view({'get': 'list'})

        request = self.factory.get(
            '/exports/submissions',
            {'format': 'csv', 'user': self.coco_user.id}
        )
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)

        received = BytesIO(b''.join(response.streaming_content)).getvalue()

        # we have filtered out the 16 new submissions, check our data
        self.assertEqual(self.expected, received)

    def test_csv_export_userprofile_filter(self):
        """
        Test CSV export userprofile filter
        """
        user = create_admin_user()

        # make 10 other random submissions
        mommy.make('main.Submission', _quantity=10)

        view = SubmissionExportViewSet.as_view({'get': 'list'})

        request = self.factory.get(
            '/exports/submissions',
            {'format': 'csv', 'userprofile': self.coco_user.userprofile.id}
        )
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)

        received = BytesIO(b''.join(response.streaming_content)).getvalue()

        # we have filtered out the 10 new submissions, check our data
        self.assertEqual(self.expected, received)

    def test_csv_export_modified_filter(self):
        """
        Test CSV export modified filter
        """
        user = create_admin_user()

        # lets get one of the submissions we had created earlier
        the_one_submission = Submission.objects.get(pk=999)

        # make 15 other random submissions
        mommy.make('main.Submission', _quantity=15)

        view = SubmissionExportViewSet.as_view({'get': 'list'})

        # filter to only get submissions modified before the_one_submission
        request = self.factory.get(
            '/exports/submissions',
            {
                'format': 'csv',
                'modified__lte': str(the_one_submission.modified)
            }
        )
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)

        received = BytesIO(b''.join(response.streaming_content)).getvalue()

        # we have filtered out the 15 new submissions, check our data
        self.assertEqual(self.expected, received)

    def test_csv_export_status_filter(self):
        """
        Test CSV export status filter
        """
        user = create_admin_user()

        # make 10 other random submissions
        mommy.make('main.Submission', _quantity=10, status=Submission.PENDING)

        view = SubmissionExportViewSet.as_view({'get': 'list'})

        request = self.factory.get(
            '/exports/submissions',
            {'format': 'csv', 'status': Submission.APPROVED}
        )
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)

        received = BytesIO(b''.join(response.streaming_content)).getvalue()

        # we have filtered out the 10 new submissions, check our data
        self.assertEqual(self.expected, received)

    def test_export_submision_time_filter(self):
        """
        Test export submission_time filter
        """
        user = create_admin_user()
        location = mommy.make('main.Location', name='Voi')

        # NOTE: we already have two submission created in the setUp method
        # their submission time value is 2018-09-04

        # make 5 other random submissions with submission_time = 2018-09-06
        mommy.make(
            'main.Submission',
            _quantity=5,
            task=self.task,
            location=location,
            user=self.coco_user,
            submission_time=parse("2018-09-06T00:00:00+03:00"),
            status=Submission.PENDING)

        # make 10 other random submissions with submission_time = 2018-09-07
        mommy.make(
            'main.Submission',
            _quantity=10,
            task=self.task,
            location=location,
            user=self.coco_user,
            submission_time=parse("2018-09-07T00:00:00+03:00"),
            status=Submission.APPROVED)

        # make 15 other random submissions with submission_time = 2018-09-08
        mommy.make(
            'main.Submission',
            _quantity=15,
            task=self.task,
            location=location,
            user=self.coco_user,
            submission_time=parse("2018-09-08T00:00:00+03:00"),
            status=Submission.REJECTED)

        # make 20 other random submissions with submission_time = 2018-09-09
        mommy.make(
            'main.Submission',
            _quantity=20,
            task=self.task,
            location=location,
            user=self.coco_user,
            submission_time=parse("2018-09-09T00:00:00+03:00"),
            status=Submission.APPROVED)

        view = SubmissionExportViewSet.as_view({'get': 'list'})

        # let us try and get submissions made on or before 2018-09-07
        request = self.factory.get(
            '/exports/submissions',
            {
                'format': 'json',
                'submission_time__lte': '2018-09-07'
            }
        )
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        # we should have 17 results
        self.assertEqual(17, len(response.data['results']))

        # let us try and get submissions made between 2018-09-06 and 2018-09-08
        request = self.factory.get(
            '/exports/submissions',
            {
                'format': 'json',
                'submission_time__gte': '2018-09-06',
                'submission_time__lte': '2018-09-08'
            }
        )
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        # we should have 20 results
        self.assertEqual(20, len(response.data['results']))

        # let us try and get submissions made after 2018-09-08
        request = self.factory.get(
            '/exports/submissions',
            {
                'format': 'json',
                'submission_time__gt': '2018-09-08'
            }
        )
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        # we should have 20 results
        self.assertEqual(20, len(response.data['results']))

    def test_csv_export_permissions_required(self):
        """
        Test CSV export permissions required
        """
        user = mommy.make('auth.User', username='somerandomuser')
        view = SubmissionExportViewSet.as_view({'get': 'list'})

        request = self.factory.get('/exports/submissions', {'format': 'csv'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(str(response.data['detail']),
                         'You shall not pass.')


class TestKaznetSubmissionViewSet(MainTestBase):
    """
    Test KaznetSubmissionViewSet class
    """

    def setUp(self):
        super().setUp()
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
        self.assertEqual(len(response.data['results']), 7)

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

        # make one submission using the user dave
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
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], submission.id)
        self.assertEqual(
            int(response.data['results'][0]['user']['id']), dave.id)

        # test dave can filter for his own submissions
        request = self.factory.get('/submissions', {'user': dave.id})
        force_authenticate(request, user=dave)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], submission.id)
        self.assertEqual(
            int(response.data['results'][0]['user']['id']), dave.id)

        # test random users can't filter for daves submissions
        request = self.factory.get('/submissions', {'user': dave.id})
        force_authenticate(request, user=random)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(str(response.data[0]['detail']),
                         'You shall not pass.')

    def test_userprofile_filter(self):
        """
        Test able to filter by userprofile
        """
        user = create_admin_user()
        random = mommy.make('auth.User')
        dave = mommy.make('auth.User', username='dave', first_name='Dave')
        daves_profile = dave.userprofile

        # make a bunch of submissions
        mommy.make('main.Submission', _quantity=7)

        # make one submission using the user dave
        submission = mommy.make('main.Submission', user=dave)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test that we get submissions for dave
        request = self.factory.get(
            '/submissions', {'userprofile': daves_profile.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], submission.id)
        self.assertEqual(
            int(response.data['results'][0]['user']['id']),
            daves_profile.user.id)

        # test dave can filter for his own submissions
        request2 = self.factory.get(
            '/submissions', {'userprofile': daves_profile.id})
        force_authenticate(request2, user=dave)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data['results']), 1)
        self.assertEqual(response2.data['results'][0]['id'], submission.id)
        self.assertEqual(
            int(response2.data['results'][0]['user']['id']),
            daves_profile.user.id)

        # test random users can't filter for daves submissions
        request3 = self.factory.get(
            '/submissions', {'userprofile': daves_profile.id})
        force_authenticate(request3, user=random)
        response3 = view(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(str(response3.data[0]['detail']),
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
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], submission.id)

        # test that we get pending submissions
        request = self.factory.get(
            '/submissions', {'status': Submission.PENDING})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 7)

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
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], submission.id)

        # test that we get not valid submissions
        request = self.factory.get('/submissions', {'valid': 0})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 7)

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
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], submission.id)

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
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], submission.id)

    def test_modified_filter(self):
        """
        Test that you can filter by modified
        """
        user = create_admin_user()
        task = mommy.make('main.Task')

        the_one_submission = mommy.make('main.Submission', task=task)

        # make a bunch of submissions
        mommy.make('main.Submission', _quantity=10, task=task)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test that we get the submission with our unique modified datetime
        request = self.factory.get(
            '/submissions', {'modified': str(the_one_submission.modified)})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['id'], the_one_submission.id)

        # test we can get submissions modified after a certain time
        request = self.factory.get(
            '/submissions', {'modified__gt': str(the_one_submission.modified)})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)

    def test_submission_time(self):
        """
        This method tests that all submissions passed through the
        serializer don't have microseconds in their submission_time
        fields and all submissions not passed through serializer
        have microseconds in their submission_time fields
        """
        now = timezone.now()
        task = mommy.make('main.Task')
        bounty = mommy.make('main.Bounty')
        location = mommy.make('main.Location')
        user = mommy.make('auth.User')
        mommy.make('main.Submission',
                   submission_time=now,
                   id=20,
                   user=user,
                   task=task,
                   bounty=bounty,
                   location=location)

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        user = create_admin_user()

        request = self.factory.get(
            '/submissions', {'id': 20})

        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)

        # ensure all the other fields have the same data
        submission = Submission.objects.filter(id=20).first()
        self.assertEqual(response.data['results'][0]['id'], submission.id)
        self.assertEqual(response.data['results'][0]['modified'],
                         submission.modified.astimezone(
            pytz.timezone(
                'Africa/Nairobi')).strftime(
            "%Y-%m-%dT%H:%M:%S.%f%z")[:-2]+":00")
        self.assertEqual(response.data['results'][0]['created'],
                         submission.created.astimezone(
            pytz.timezone(
                'Africa/Nairobi')).strftime(
            "%Y-%m-%dT%H:%M:%S.%f%z")[:-2]+":00")
        self.assertEqual(response.data['results'][0]
                         ['task']['id'], str(submission.task.id))
        self.assertEqual(response.data['results'][0]
                         ['bounty']['id'], str(submission.bounty.id))
        self.assertEqual(response.data['results'][0]['location']['id'], str(
            submission.location.id))
        self.assertEqual(response.data['results'][0]
                         ['user']['id'], str(submission.user.id))

        # ensure that the submission_timefield is exacly the same except
        # for microseconds
        self.assertEqual(response.data['results'][0]['submission_time'],
                         submission.submission_time.astimezone(
            pytz.timezone('Africa/Nairobi')).strftime(
            "%Y-%m-%dT%H:%M:%S%z")[:-2]+":00")
        self.assertFalse('.' in response.data['results'][0]['submission_time'])

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
        self.assertEqual(len(response.data['results']), 7)
        # the first record is what we expect
        # pylint: disable=no-member
        self.assertEqual(
            response.data['results'][0]['id'],
            Submission.objects.order_by('-submission_time').first().id)
        self.assertEqual(
            response.data['results'][0]['submission_time'],
            Submission.objects.order_by(
                '-submission_time').first().submission_time.astimezone(
                    pytz.timezone(
                        'Africa/Nairobi')).strftime(
                            "%Y-%m-%dT%H:%M:%S%z")[:-2]+":00")
        # the last record is what we epxect
        self.assertEqual(
            response.data['results'][-1]['id'],
            Submission.objects.order_by('-submission_time').last().id)
        self.assertEqual(
            response.data['results'][-1]['submission_time'],
            Submission.objects.order_by(
                '-submission_time').last().submission_time.astimezone(
                    pytz.timezone(
                        'Africa/Nairobi')).strftime(
                            "%Y-%m-%dT%H:%M:%S%z")[:-2]+":00")

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
        self.assertEqual(len(response.data['results']), 8)
        self.assertEqual(
            response.data['results'][0]['id'],
            Submission.objects.order_by('valid').first().id)
        self.assertEqual(len(response.data['results']), 8)
        self.assertEqual(response.data['results'][-1]['id'], submission.id)

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
        self.assertEqual(len(response.data['results']), 9)
        self.assertEqual(
            response.data['results'][0]['id'],
            submission.id)
        self.assertEqual(response.data['results'][-1]['id'], submission1.id)

    def test_submission_modified_sorting(self):
        """
        Test that we can Order By Modified
        """
        user = create_admin_user()

        submission1 = mommy.make('main.Submission')

        # make a bunch of Submissions
        mommy.make('main.Submission', _quantity=7)

        submission2 = mommy.make('main.Submission')

        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        # test sorting in descending order by modified
        request = self.factory.get(
            '/submissions', {'ordering': '-modified'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 9)

        self.assertEqual(
            parse(response.data['results'][-1]['modified']).astimezone(
                pytz.utc),
            submission1.modified)
        self.assertEqual(response.data['results'][-1]['id'], submission1.id)
        self.assertEqual(
            parse(
                response.data['results'][0]['modified']).astimezone(pytz.utc),
            submission2.modified)
        self.assertEqual(response.data['results'][0]['id'], submission2.id)
        self.assertTrue(
            response.data['results'][-1]['modified'] <
            response.data['results'][0]['modified']
        )

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
            str(response2.data[0]['detail']))

        # test that you need authentication for listing submissions
        view3 = KaznetSubmissionsViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/submissions')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response3.data[0]['detail']))

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
        self.assertEqual(str(response.data[0]['detail']),
                         'You shall not pass.')

        # Can't list all submissions
        view = KaznetSubmissionsViewSet.as_view({'get': 'list'})

        request = self.factory.get('/submissions')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(str(response.data[0]['detail']),
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
        self.assertEqual(int(response.data['user']['id']), user.id)
