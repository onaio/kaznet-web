"""
Test renderers
"""
from types import GeneratorType

from dateutil import parser
from django_prices.models import Money
from model_mommy import mommy
from rest_framework.test import APIRequestFactory

from kaznet.apps.main.renderers import CSVStreamingRenderer
from kaznet.apps.main.models import Submission
from kaznet.apps.main.serializers import SubmissionExportSerializer
from kaznet.apps.main.tests.base import MainTestBase


class TestCSVStreamingRenderer(MainTestBase):
    """
    Tests CSVStreamingRenderer
    """

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        task = mommy.make('main.Task', name='Quest')
        mommy.make(
            'main.Submission',
            task=task,
            location=mommy.make('main.Location', name='Voi'),
            user=mommy.make('auth.User', first_name='Coco'),
            bounty=mommy.make(
                'main.Bounty',
                task=task,
                amount=Money('50', 'KES')),
            submission_time=parser.parse("2018-09-04T03:39:29+00:00"),
            id=555
        )
        mommy.make(
            'main.Submission',
            task=task,
            location=mommy.make('main.Location', name='Voi'),
            user=mommy.make('auth.User', first_name='Coco'),
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
        expected = "id,user,task,location,submission_time,approved,status,comments,amount,currency,phone_number,payment_number\r\n555,Coco,Quest,Voi,2018-09-04T03:39:29+00:00,,d,,50.00,KES,,\r\n666,Coco,Quest,Voi,2018-09-04T03:39:29+00:00,,d,,50.00,KES,,\r\n"  # noqa

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
