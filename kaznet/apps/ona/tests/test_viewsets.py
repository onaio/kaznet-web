"""
Module containing all tests for Ona Apps
viewsets.py
"""
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.ona.viewsets import XFormViewSet
from kaznet.apps.users.tests.base import create_admin_user


class TestXFormViewSet(TestCase):
    """
    Tests for XFormViewSet
    """

    def setUp(self):
        super(TestXFormViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def test_list_xfrom(self):
        """
        Test that GET /xforms returns a list of all xforms
        """
        user = create_admin_user()
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'list'})

        request = self.factory.get('/xforms')
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(4, len(response.data))

    def test_retrieve_xfrom(self):
        """
        Test that GET /xforms/[id] returns a specific item
        matching pk
        """
        user = create_admin_user()
        form = mommy.make('ona.XForm', title="Form A")
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get('/xforms/{id}'.format(id=form.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=form.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.id, response.data['id'])
        self.assertEqual(form.title, response.data['title'])

    def test_authentication_required(self):
        """
        Test that user has to be authenticated in order to
        make requests
        """
        # Requires Authentication to List
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'list'})

        request = self.factory.get('/xforms')
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.data['detail']
        )

        # Requires Authentication to Retrieve
        form = mommy.make('ona.XForm', title="Form A")
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get('/xforms/{id}'.format(id=form.id))
        response = view(request=request, pk=form.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.data['detail']
        )

    def test_permission_required(self):
        """
        Test that user has to be an Admin to access API
        """
        # Requires permission to List
        user = mommy.make('auth.User')
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'list'})

        request = self.factory.get('/xforms')
        force_authenticate(request, user)
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            response.data['detail']
        )

        # Requires permission to Retrieve
        form = mommy.make('ona.XForm', title="Form A")
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get('/xforms/{id}'.format(id=form.id))
        force_authenticate(request, user)
        response = view(request=request, pk=form.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            response.data['detail']
        )