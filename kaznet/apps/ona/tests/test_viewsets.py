"""
Module containing all tests for Viewsets in
Ona App
"""
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.ona.viewsets import XFormViewSet


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
        user = mommy.make('auth.User')
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'list'})

        requester = self.factory.get('/xforms')
        force_authenticate(requester, user=user)
        response = view(request=requester)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(4, len(response.data))

    def test_retrieve_xfrom(self):
        """
        Test that GET /xforms/[id] returns a specific item
        matching pk
        """
        user = mommy.make('auth.User')
        form = mommy.make('ona.XForm', title="Form A")
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'retrieve'})

        requester = self.factory.get('/xforms/{id}'.format(id=form.id))
        force_authenticate(requester, user=user)
        response = view(request=requester, pk=form.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.id, response.data['id'])
        self.assertEqual(form.title, response.data['title'])
