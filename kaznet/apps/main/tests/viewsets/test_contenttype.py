"""
Tests for  ContentType viewsets.
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.main.viewsets import ContentTypeViewSet


class TestContentTypeViewSet(MainTestBase):
    """
    Test LocationViewSet class.
    """

    def setUp(self):
        super(TestContentTypeViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def test_list_contenttype(self):
        """
        Test that we can get the list of allowed content types
        """
        user = mommy.make('auth.User')
        view = ContentTypeViewSet.as_view({'get': 'list'})

        request = self.factory.get('/contenttypes')
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.data['results']), get_allowed_contenttypes().count())
        self.assertTrue(
            ContentType.objects.filter(
                pk=response.data['results'][1]['id']).exists())

    def test_authentication_required(self):
        """
        Test that authentication is required to access API Endpoint
        """
        view = ContentTypeViewSet.as_view({'get': 'list'})

        request = self.factory.get('/contenttypes')
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data[0]['detail']))
