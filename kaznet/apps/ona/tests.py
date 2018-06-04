"""
Tests for ona app
"""
from unittest.mock import patch
from urllib.parse import urljoin

from django.test import TestCase
from django.utils.text import slugify

import requests_mock
from model_mommy import mommy
from requests.exceptions import RetryError
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.ona.api import (get_instances, get_projects, process_instance,
                                 process_instances, process_project,
                                 process_projects, process_xform,
                                 process_xforms, request, request_session)
from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.apps.ona.serializers import (InstanceSerializer, ProjectSerializer,
                                         XFormSerializer)
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


class TestApiMethods(TestCase):
    """
    Tests for the API Methods
    """

    @requests_mock.Mocker()
    def test_get_projects(self, mocked):
        """
        Test to see that get_projects returns the
        correct data
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
            f'{ONA_BASE_URL}/api/v1/projects?owner=kaznettest',
            json=mocked_projects_data
            )
        response = get_projects()

        self.assertEqual(response, mocked_projects_data)

    @requests_mock.Mocker()
    def test_get_instances(self, mocked):
        """
        Test to see that get_instances returns
        the correct data
        """
        mocked_instances = [
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": True,
                "_last_edited": "2018-05-30T07:51:59.187363Z",
                "_xform_id": 53,
                "_id": 1755
            }
        ]
        form = mommy.make('ona.XForm', ona_pk=1755)
        mocked.get(
            f'{ONA_BASE_URL}/api/v1/data/1755?start=0&limit=100',
            json=mocked_instances
        )
        mocked.get(
            f'{ONA_BASE_URL}/api/v1/data/1755?start=100&limit=100',
            json=[]
        )

        response = get_instances(form)

        self.assertEqual(response, mocked_instances)

    # pylint: disable=no-self-use
    @patch('kaznet.apps.ona.api.process_project')
    def test_processprojects(self, mockclass):
        """
        Test that process_projects works the way it
        should when given proper and improper data
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

        # Test that when valid projects data is passed it calls process_project
        process_projects(mocked_projects_data)
        mockclass.assert_called_with(mocked_projects_data[0])

        # Test that when invalid projects data is passed it does nothing
        mocked_projects_data = None
        process_projects(mocked_projects_data)

        mockclass.assert_called_once()

    def test_processproject_good_data(self):
        """
        Test that when process_project is given proper data it creates
        an object
        """
        project_data = {
            "projectid": 18,
            "name": "Changed2",
            "date_modified": "2018-05-30T07:51:59.267839Z",
            "deleted_at": None
        }

        self.assertEqual(len(Project.objects.all()), 0)
        process_project(project_data)
        self.assertEqual(len(Project.objects.all()), 1)

    def test_processproject_bad_data(self):
        """
        Test that when process_project is given proper data it
        does not create an object
        """
        project_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False
        }

        current = len(Project.objects.all())
        process_project(project_data)

        self.assertEqual(len(Project.objects.all()), current)

    @patch('kaznet.apps.ona.api.process_xform')
    def test_processxforms(self, mockclass):
        """
        Test that process_xforms works the way it
        should when given proper and improper data
        """
        mocked_forms_data = [
            {
                "name": "Changed",
                "formid": 53,
                "id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "is_merged_dataset": False
            }
        ]

        # Test that when valid forms data is passed it calls process_xform
        process_xforms(mocked_forms_data, 18)
        mockclass.assert_called_with(mocked_forms_data[0], 18)

        # Test that when invalid projects data is passed it does nothing
        mocked_forms_data = None

        process_xforms(mocked_forms_data, 18)
        mockclass.assert_called_once()

    def test_processxform_good_data(self):
        """
        Test that when process_xform is called with valid dat
        it creates an XForm Object
        """
        mocked_form_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False
        }

        self.assertEqual(len(XForm.objects.all()), 0)
        process_xform(mocked_form_data, 18)

        self.assertEqual(len(XForm.objects.all()), 1)

    def test_processxform_bad_data(self):
        """
        Test that when process_xform is called with valid dat
        it creates an XForm Object
        """
        mocked_form_data = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-05-30T07:51:59.187363Z",
            "_xform_id": 53,
            "_id": 1755
        }
        current = len(XForm.objects.all())
        process_xform(mocked_form_data, 18)

        self.assertEqual(len(XForm.objects.all()), current)

    @patch('kaznet.apps.ona.api.process_instance')
    def test_processinstances(self, mockclass):
        """
        Test that process_instances calls process_instance
        """
        mocked_instances = [
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": True,
                "_last_edited": "2018-05-30T07:51:59.187363Z",
                "_xform_id": 53,
                "_id": 1755
            }
        ]

        mocked_xform = mommy.make('ona.XForm', ona_pk=1755)

        # Test that when valid forms data is passed it calls process_instance
        process_instances(mocked_instances, mocked_xform)
        mockclass.assert_called_with(mocked_instances[0], mocked_xform)

    def test_processinstance_good_data(self):
        """
        Test that when process_instance is called with valid dat
        it creates an Instance Object
        """
        mocked_instance_data = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-05-30T07:51:59.187363Z",
            "_xform_id": 53,
            "_id": 1755
        }

        mocked_xform = mommy.make('ona.XForm', ona_pk=1755)

        self.assertEqual(len(Instance.objects.all()), 0)
        process_instance(mocked_instance_data, mocked_xform)

        self.assertEqual(len(Instance.objects.all()), 1)

    def test_processinstance_bad_data(self):
        """
        Test that when process_instance is called with invalid data
        it doesn't create an Instance Object
        """
        mocked_instance_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False
        }

        mocked_xform = mommy.make('ona.XForm', ona_pk=1755)

        self.assertEqual(len(Instance.objects.all()), 0)
        process_instance(mocked_instance_data, mocked_xform)

        self.assertEqual(len(Instance.objects.all()), 0)

    @requests_mock.Mocker()
    def test_request(self, mocked):
        """
        Test that request returns correct json data when given
        valid url and args
        """
        mocked_response = [
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": False,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1755
            }
        ]
        mocked.get(
            f'{ONA_BASE_URL}/api/v1/data/53',
            json=mocked_response
            )
        url = urljoin(ONA_BASE_URL, 'api/v1/data/53')
        response = request(url)

        self.assertEqual(mocked_response, response)

    @requests_mock.Mocker()
    def test_request_bad_data(self, mocked):
        """
        Test that request returns None for Incorrect Data
        """
        mocked.get(
            f'{ONA_BASE_URL}/api/v1/data/53',
            text='Oh! Hello There!'
            )
        url = urljoin(ONA_BASE_URL, 'api/v1/data/53')
        response = request(url)

        self.assertEqual(response, None)

    def test_requests_session(self):
        """
        Tests that a valid url can be accessed normally
        """
        response = request_session('https://example.com', 'GET')
        self.assertTrue(response.status_code, 200)

    def test_requests_session_bad_url(self):
        """
        Test that an invalid url will fail
        eventually
        """
        with self.assertRaises(RetryError):
            request_session(
                url='http://httpbin.org/status/500',
                method='GET',
                retries=3,
                backoff_factor=0
                )

        with self.assertRaises(RetryError):
            request_session(
                url='http://httpbin.org/status/502',
                method='GET',
                retries=3,
                backoff_factor=0
                )

        with self.assertRaises(RetryError):
            request_session(
                url='http://httpbin.org/status/504',
                method='GET',
                retries=3,
                backoff_factor=0
                )
