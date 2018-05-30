"""
Tests for ona app
"""
from unittest.mock import patch

from django.test import TestCase
from django.utils.text import slugify

import requests_mock
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.ona.api import (get_instances, get_projects, get_xform,
                                 process_instance, process_project,
                                 process_xform, requests_session)
from kaznet.apps.ona.models import OnaInstance, OnaProject, XForm
from kaznet.apps.ona.serializers import (OnaInstanceSerializer,
                                         OnaProjectSerializer, XFormSerializer)
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


class TestOnaProjectModel(TestCase):
    """
    Tests for OnaProjectModel
    """

    def test_onaproject_str(self):
        """
        Test string representation for OnaProject Model
        """
        project = mommy.make('ona.OnaProject', name='Project Zero')
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
            'ona_project_id': 54,
            'title': 'Solar Flare',
            'id_string': mocked_idstring
        }

        serializer_data = XFormSerializer(mocked_data).data
        expected_fields = {
            'id',
            'ona_pk',
            'ona_project_id',
            'id_string',
            'deleted_at',
            'title',
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))

        self.assertEqual(596, serializer_data['ona_pk'])
        self.assertEqual(54, serializer_data['ona_project_id'])
        self.assertEqual("Solar Flare", serializer_data['title'])
        self.assertEqual(mocked_idstring, serializer_data['id_string'])


class TestOnaInstanceSerializer(TestCase):
    """
    Tests for OnaInstanceSerializer
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

        serializer_data = OnaInstanceSerializer(mocked_data).data

        expected_fields = {
            'id',
            'ona_pk',
            'xform',
            'json',
            'deleted_at'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))
        self.assertEqual(596, serializer_data['ona_pk'])
        self.assertEqual(mocked_xform.id, serializer_data['xform'])
        self.assertEqual(dict, serializer_data['json'])


class TestOnaProjectSerializer(TestCase):
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
            'ona_organization': 12,
            'name': 'Project Zero'
        }

        serializer_data = OnaProjectSerializer(mocked_data).data

        expected_fields = {
            'id',
            'ona_pk',
            'ona_organization',
            'name',
            'deleted_at'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))

        self.assertEqual(59, serializer_data['ona_pk'])
        self.assertEqual(12, serializer_data['ona_organization'])
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


class ApiModule(TestCase):
    """
    Tests for the Api module in Ona App
    """

    def test_requests_session(self):
        """
        Tests that a valid url can be accessed normally
        """
        response = requests_session('https://example.com')
        self.assertTrue(response.status_code, 200)

    # pylint: disable=no-self-use
    @patch('kaznet.apps.ona.api.process_project')
    @requests_mock.Mocker()
    def test_get_projects(self, mockclass, mocked):
        """
        Test to see that get projects
        """
        mocked_projects_data = [
            {
                "projectid": 18,
                "forms": [
                    {
                        "name": "Changed",
                        "formid": 53,
                        "id_string": "aFEjJKzULJbQYsmQzKcpL9",
                        "is_merged_dataset": False}
                    ],
                "name": "Changed2",
                "date_modified": "2018-05-30T07:51:59.267839Z",
                "deleted_at": None
            }
        ]

        mocked.get(
            f'{ONA_BASE_URL}/projects?owner=',
            json=mocked_projects_data
            )

        get_projects('kaznettest')
        mockclass.assert_called_with(mocked_projects_data[0])

    @patch('kaznet.apps.ona.api.process_xform')
    def test_process_project(self, mockclass):
        """
        Test to see that process_project will create an OnaProject
        object and call process_xform with correct data after getting
        its input.
        """
        current = len(OnaProject.objects.all()) + 1
        mocked_project_data = {
            "projectid": 18,
            "forms": [
                {
                    "name": "Changed",
                    "formid": 53,
                    "id_string": "aFEjJKzULJbQYsmQzKcpL9",
                    "is_merged_dataset": False
                    }
                ],
            "name": "Changed2",
            "date_modified": "2018-05-30T07:51:59.267839Z",
            "deleted_at": None
            }

        process_project(mocked_project_data)
        mockclass.assert_called_with(mocked_project_data['forms'][0], 18)
        self.assertEqual(len(OnaProject.objects.all()), current)

    @patch('kaznet.apps.ona.api.get_instances')
    def test_process_xform(self, mockclass):
        """
        Test to see that process_xform will create an XForm and
        call get_instances with correct data after getting
        its input.
        """
        current = len(XForm.objects.all()) + 1
        mocked_xform_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False
        }

        process_xform(mocked_xform_data, 18)
        obj = XForm.objects.get(ona_pk=53)
        mockclass.assert_called_with(obj)

        self.assertEqual(len(XForm.objects.all()), current)

    @patch('kaznet.apps.ona.api.process_instance')
    @requests_mock.Mocker()
    def test_get_instances(self, mockclass, mocked):
        """
        Test to see that get_instances will call
        process_instance with correct data after getting
        its input.
        """
        mocked_instances = [
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": True,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1755
            }
        ]
        form = mommy.make('ona.XForm', ona_pk=1755)
        mocked.get(
            f'{ONA_BASE_URL}/data/1755?start=0&limit=100',
            json=mocked_instances
            )
        mocked.get(
            f'{ONA_BASE_URL}/data/1755?start=100&limit=100',
            json=[]
        )
        get_instances(form)
        mockclass.assert_called_with(mocked_instances[0], form)

    def test_process_instance(self):
        """
        Test to see that get_instances will save the instance
        after getting its input.
        """
        current = len(OnaInstance.objects.all()) + 1
        obj = mommy.make('ona.XForm', ona_pk=53)
        instance_data = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-05-30T07:51:59.187363+00:00",
            "_xform_id": 53,
            "_id": 1755
        }
        process_instance(instance_data, obj)

        self.assertEqual(len(OnaInstance.objects.all()), current)

    @patch('kaznet.apps.ona.api.get_instances')
    @requests_mock.Mocker()
    def test_get_xform(self, mockclass, mocked):
        """
        Test to see that process_xform will create an XForm and
        call get_instances with correct data after getting
        its input.
        """
        current = len(XForm.objects.all()) + 1
        mocked_xform_data = {
            "title": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "last_updated_at": "2018-05-30T06:47:23.196149Z",
        }
        mocked.get(
            f'{ONA_BASE_URL}/forms/53', json=mocked_xform_data
            )

        obj = mommy.make('ona.OnaProject')
        get_xform(53, obj)
        mocked_form = XForm.objects.get(ona_pk=53)

        mockclass.assert_called_with(mocked_form)
        self.assertEqual(len(XForm.objects.all()), current)
