"""
Tests for ona app
"""
from unittest.mock import patch

from django.test import TestCase
from django.utils.text import slugify

import requests_mock
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.apps.ona.serializers import (InstanceSerializer,
                                         ProjectSerializer, XFormSerializer)
from kaznet.apps.ona.viewsets import XFormViewSet
from kaznet.settings.common import ONA_BASE_URL


class TestXFormModel(TestCase):
    """
    Tests for XFormModel
    """

    def test_xform_str(self):
        """
        Test string representation for XForm Model
        """
        xform = mommy.make('ona.XForm', title='Test')
        self.assertEqual(str(xform), 'Test')


class TestProjectModel(TestCase):
    """
    Tests for ProjectModel
    """

    def test_project_str(self):
        """
        Test string representation for Project Model
        """
        project = mommy.make('ona.Project', name='Project Zero')
        self.assertEqual(str(project), 'Project Zero')


class TestXFormSerializer(TestCase):
    """
    Tests for XFromSerializer
    """

    def test_serializer_output(self):
        """
        Test that we get fields we are exprecting
        """
        mocked_idstring = slugify('Solar Flare')
        mocked_data = {
            'id': 45,
            'ona_pk': 596,
            'project_id': 54,
            'title': 'Solar Flare',
            'id_string': mocked_idstring
        }

        serializer_data = XFormSerializer(mocked_data).data
        expected_fields = {
            'id',
            'ona_pk',
            'project_id',
            'last_updated',
            'id_string',
            'deleted_at',
            'title',
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))

        self.assertEqual(596, serializer_data['ona_pk'])
        self.assertEqual(54, serializer_data['project_id'])
        self.assertEqual("Solar Flare", serializer_data['title'])
        self.assertEqual(mocked_idstring, serializer_data['id_string'])


class TestInstanceSerializer(TestCase):
    """
    Tests for InstanceSerializer
    """

    def test_serializer_output(self):
        """
        Test that we get the fields we are expecting
        """
        mocked_xform = mommy.make('ona.XForm')
        mocked_data = {
            'id': 34,
            'ona_pk': 596,
            'xform': mocked_xform,
            'json': dict
        }

        serializer_data = InstanceSerializer(mocked_data).data

        expected_fields = {
            'id',
            'ona_pk',
            'xform',
            'last_updated',
            'json',
            'deleted_at'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))
        self.assertEqual(596, serializer_data['ona_pk'])
        self.assertEqual(mocked_xform.id, serializer_data['xform'])
        self.assertEqual(dict, serializer_data['json'])


class TestProjectSerializer(TestCase):
    """
    Tests for OnaProjectSerializer
    """

    def test_serializer_output(self):
        """
        Test that we get the fields we are expecting
        """
        mocked_data = {
            'id': 1,
            'ona_pk': 59,
            'organization': 12,
            'name': 'Project Zero'
        }

        serializer_data = ProjectSerializer(mocked_data).data

        expected_fields = {
            'id',
            'ona_pk',
            'organization',
            'last_updated',
            'name',
            'deleted_at'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))

        self.assertEqual(59, serializer_data['ona_pk'])
        self.assertEqual(12, serializer_data['organization'])
        self.assertEqual('Project Zero', serializer_data['name'])


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
        user = mommy.make('auth.User')
        form = mommy.make('ona.XForm', title="Form A")
        mommy.make('ona.XForm', _quantity=4)
        view = XFormViewSet.as_view({'get': 'retrieve'})

        request = self.factory.get('/xforms/{id}'.format(id=form.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=form.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.id, response.data['id'])
        self.assertEqual(form.title, response.data['title'])
