"""
Module containing all tests for Ona App
Views
"""
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIRequestFactory

from kaznet.apps.ona.views import create_instance
from kaznet.apps.ona.models import Instance


class TestViews(TestCase):
    """
    Tests for views.py
    """

    def setUp(self):
        super(TestViews, self).setUp()
        self.factory = APIRequestFactory()
        self.user = mommy.make(
            'auth.User',
            username='sluggie'
        )

    def test_create_instance(self):
        """
        Test create_instance api view returns a Response 201
        When passed in correct data
        """
        instance_data = {
            '_xform_id_string': 'aFEjJKzULJbQYsmQzKcpL9',
            '_edited': True,
            '_last_edited': '2018-05-30T07:51:59.187363Z',
            '_xform_id': 53,
            '_submitted_by': 'sluggie',
            '_id': 1755
        }

        xfrom = mommy.make('ona.XForm', ona_pk=53)

        request = self.factory.post(
            'api/v1/create_instance', data=instance_data)
        self.assertEqual(Instance.objects.all().count(), 0)
        response = create_instance(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(Instance.objects.all().count(), 1)
