"""
Module containing all tests for Ona App
Views
"""
import json

from model_mommy import mommy
from rest_framework.test import APIRequestFactory

from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.models import Instance
from kaznet.apps.ona.views import create_or_update_instance


class TestViews(MainTestBase):
    """
    Tests for views.py
    """

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.user = mommy.make(
            'auth.User',
            username='sluggie'
        )

    def test_create_or_update_instance(self):
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

        mommy.make('ona.XForm', ona_pk=53)

        request = self.factory.post(
            'webhook',
            data=json.dumps(instance_data),
            content_type='application/json'
        )
        self.assertEqual(Instance.objects.all().count(), 0)
        response = create_or_update_instance(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(Instance.objects.all().count(), 1)
