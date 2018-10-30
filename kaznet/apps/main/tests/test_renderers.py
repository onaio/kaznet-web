"""
Test renderers
"""
from types import GeneratorType

from dateutil import parser
from django_prices.models import Money
from model_mommy import mommy
from rest_framework.test import APIRequestFactory

from kaznet.apps.main.renderers import CSVStreamingRenderer
from kaznet.apps.main.models import Submission, Task, Location
from kaznet.apps.main.serializers import SubmissionExportSerializer
from kaznet.apps.main.tests.base import MainTestBase


class TestCSVStreamingRenderer(MainTestBase):
    """
    Tests CSVStreamingRenderer
    """

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        try:
            self.task = Task.objects.get(id=2001)
        except Task.DoesNotExist:

            task = mommy.make('main.Task', name='Quest')
            task.id = 2001
            task.save(force_insert=True)
            self.task = task

        try:
            self.location = Location.objects.get(id=3001)
        except Location.DoesNotExist:

            location = mommy.make('main.Location', name='Voi')
            location.id = 3001
            location.save(force_insert=True)
            self.location = location
            self.coco_user = mommy.make('auth.User', first_name='Coco', id=1001)
        mommy.make(
            'main.Submission',
            task=self.task,
            location=self.location,
            user=self.coco_user,
            bounty=mommy.make(
                'main.Bounty',
                task=task,
                amount=Money('50', 'KES')),
            submission_time=parser.parse("2018-09-04T03:39:29+00:00"),
            id=555
        )
        mommy.make(
            'main.Submission',
            task=self.task,
            location=self.location,
            user=self.coco_user,
            bounty=mommy.make(
                'main.Bounty',
                task=task,
                amount=Money('50', 'KES')),
            submission_time=parser.parse("2018-09-04T03:39:29+00:00"),
            id=666
        )
        self.data = Submission.objects.filter(id__in=[555, 666])

    def test_renderer_return_type(self):
        """
        Test the return type
        """
        renderer = CSVStreamingRenderer()
        dump = renderer.render(self.data)
        self.assertIsInstance(dump, GeneratorType)

    def test_renderer_value(self):
        """
        Test that we get the right data back
        """
        expected = "id,user,user_id,task,task_id,location,location_id,submission_time,approved,status,comments,amount,currency,phone_number,payment_number\r\n555,Coco,1001,Quest,2001,Voi,3001,2018-09-04T03:39:29+00:00,,d,,50.00,KES,,\r\n666,Coco,1001,Quest,2001,Voi,3001,2018-09-04T03:39:29+00:00,,d,,50.00,KES,,\r\n"  # noqa

        streaming_renderer = CSVStreamingRenderer()
        request = self.factory.get('/exports/submissions?format=csv')
        streaming_renderer_data = ''.join(
            streaming_renderer.render(
                {
                    'queryset': self.data,
                    'serializer': SubmissionExportSerializer,
                    'context': {'request': request}
                }
            )
        )

        self.assertEqual(
            expected,
            streaming_renderer_data
        )
