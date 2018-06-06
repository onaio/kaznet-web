"""
Module containing tests for
Ona Apps api.py methods
"""

from unittest.mock import patch
from urllib.parse import urljoin

from django.test import TestCase

import requests_mock
from model_mommy import mommy
from requests.exceptions import RetryError
# pylint: disable=import-error
from requests.packages.urllib3.util.retry import Retry

from kaznet.apps.ona.api import (get_instance, get_instances, get_project,
                                 get_project_obj, get_projects, get_xform,
                                 get_xform_obj, process_instance,
                                 process_instances, process_project,
                                 process_projects, process_xform,
                                 process_xforms, request, request_session)
from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.settings.common import ONA_BASE_URL


# pylint: disable=too-many-public-methods
class TestApiMethods(TestCase):
    """
    Tests for the API Methods
    """

    def setUp(self):
        self.user = mommy.make(
            'auth.User',
            username='sluggie'
        )

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
            urljoin(ONA_BASE_URL, 'api/v1/projects?owner=kaznettest'),
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
        mocked.get(
            urljoin(ONA_BASE_URL, '/api/v1/data/53?start=0&limit=100'),
            json=mocked_instances
        )
        mocked.get(
            urljoin(ONA_BASE_URL, '/api/v1/data/53?start=100&limit=100'),
            json=[]
        )

        response = get_instances(53)
        for i in response:
            mocked_data = i
        self.assertEqual(mocked_data, mocked_instances)

    @requests_mock.Mocker()
    def test_get_project(self, mocked):
        """
        Test to see that get_project returns the correct
        data
        """
        mocked_project_data = {
            "projectid": 18,
            "name": "Changed2",
            "date_modified": "2018-05-30T07:51:59.267839Z",
            "deleted_at": None
        }

        url = urljoin(ONA_BASE_URL, 'api/v1/projects/18')
        mocked.get(
            url,
            json=mocked_project_data
            )
        response = get_project(url)

        self.assertTrue(response, mocked_project_data)

    @requests_mock.Mocker()
    def test_get_xform(self, mocked):
        """
        Test to see that get_xform returns the correct
        data
        """
        mocked_xform_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False
        }

        url = urljoin(ONA_BASE_URL, 'api/v1/forms/53')
        mocked.get(
            url,
            json=mocked_xform_data
            )
        response = get_xform(53)

        self.assertTrue(response, mocked_xform_data)

    @requests_mock.Mocker()
    def test_get_instance(self, mocked):
        """
        Test to see that get_instance returns the correct
        data
        """
        mocked_instance_data = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-05-30T07:51:59.187363Z",
            "_xform_id": 53,
            "_id": 1755
        }

        url = urljoin(ONA_BASE_URL, 'api/v1/data/53/142')
        mocked.get(
            url,
            json=mocked_instance_data
            )
        response = get_instance(53, 142)
        self.assertTrue(response, mocked_instance_data)

    # pylint: disable=no-self-use
    @patch('kaznet.apps.ona.api.process_project')
    def test_process_projects(self, mockclass):
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

    def test_process_project_good_data(self):
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

        self.assertEqual(Project.objects.all().count(), 0)
        process_project(project_data)
        self.assertEqual(Project.objects.all().count(), 1)

    def test_process_project_bad_data(self):
        """
        Test that when process_project is given improper data it
        does not create an object
        """
        project_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False
        }

        process_project(project_data)

        self.assertEqual(Project.objects.all().count(), 0)

    @patch('kaznet.apps.ona.api.process_xform')
    def test_process_xforms(self, mockclass):
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
        mockclass.assert_called_with(mocked_forms_data[0], project_id=18)

        # Test that when invalid projects data is passed it does nothing
        mocked_forms_data = None

        process_xforms(mocked_forms_data, project_id=18)
        mockclass.assert_called_once()

    @requests_mock.Mocker()
    def test_process_xform_good_data(self, mocked):
        """
        Test that when process_xform is called with valid data
        it creates an XForm Object and a Project Object
        If its not present
        """
        mocked_form_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False
        }

        mocked_project_data = {
            "projectid": 18,
            "name": "Changed2",
            "date_modified": "2018-05-30T07:51:59.267839Z",
            "deleted_at": None
        }

        mocked.get(
            urljoin(ONA_BASE_URL, '/api/v1/projects/18'),
            json=mocked_project_data
        )

        self.assertEqual(XForm.objects.all().count(), 0)
        self.assertEqual(Project.objects.all().count(), 0)
        process_xform(mocked_form_data, 18)

        self.assertEqual(XForm.objects.all().count(), 1)
        self.assertEqual(Project.objects.all().count(), 1)

    def test_process_xform_bad_data(self):
        """
        Test that when process_xform is called with valid data
        it creates an XForm Object
        """
        mocked_form_data = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-05-30T07:51:59.187363Z",
            "_xform_id": 53,
            "_id": 1755
        }
        process_xform(mocked_form_data, 18)

        self.assertEqual(Project.objects.all().count(), 0)
        self.assertEqual(XForm.objects.all().count(), 0)

    @patch('kaznet.apps.ona.api.process_instance')
    def test_process_instances(self, mockclass):
        """
        Test that process_instances calls process_instance
        """
        mocked_instances = (
            [
                [
                    {
                        "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                        "_edited": True,
                        "_last_edited": "2018-05-30T07:51:59.187363Z",
                        "_xform_id": 53,
                        "_submitted_by": "sluggie",
                        "_id": 1755
                    }
                ]
            ]
        )

        mocked_xform = mommy.make('ona.XForm', ona_pk=1755)

        # Test that when valid forms data is passed it calls process_instance
        process_instances(mocked_instances, mocked_xform)
        mockclass.assert_called_with(mocked_instances[0][0], mocked_xform)

    @requests_mock.Mocker()
    def test_process_instance_good_data(self, mocked):
        """
        Test that when process_instance is called with valid data
        it creates an Instance Object as well as an XForm object and a Project
        Object if not present.
        """
        mocked_instance_data = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-05-30T07:51:59.187363Z",
            "_xform_id": 53,
            "_submitted_by": "sluggie",
            "_id": 1755
        }

        mocked_form_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False,
            "project": "https://stage-api.ona.io/api/v1/projects/18"
        }

        mocked_project_data = {
            "projectid": 18,
            "name": "Changed2",
            "date_modified": "2018-05-30T07:51:59.267839Z",
            "deleted_at": None
        }

        mocked.get(
            urljoin(ONA_BASE_URL, '/api/v1/projects/18'),
            json=mocked_project_data
        )

        mocked.get(
            urljoin(ONA_BASE_URL, '/api/v1/forms/53'),
            json=mocked_form_data
        )
        self.assertEqual(Instance.objects.all().count(), 0)
        self.assertEqual(XForm.objects.all().count(), 0)
        self.assertEqual(Project.objects.all().count(), 0)

        process_instance(mocked_instance_data)

        self.assertEqual(Instance.objects.all().count(), 1)
        self.assertEqual(XForm.objects.all().count(), 1)
        self.assertEqual(Project.objects.all().count(), 1)

    def test_process_instance_bad_data(self):
        """
        Test that when process_instance is called with invalid data
        it doesn't create an Instance Object or an XForm Object
        """
        # TODO: submitted by with bad data
        mocked_instance_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False
        }
        process_instance(mocked_instance_data)

        self.assertEqual(Instance.objects.all().count(), 0)
        self.assertEqual(XForm.objects.all().count(), 0)

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
        url = urljoin(ONA_BASE_URL, 'api/v1/data/53')
        mocked.get(
            url,
            json=mocked_response
            )
        response = request(url)

        self.assertEqual(mocked_response, response)

    @requests_mock.Mocker()
    def test_request_bad_data(self, mocked):
        """
        Test that request returns None for Incorrect Data
        """
        url = urljoin(ONA_BASE_URL, 'api/v1/data/53')
        mocked.get(
            url,
            text='Oh! Hello There!'
            )
        response = request(url)

        self.assertEqual(response, None)

    def test_request_session(self):
        """
        Tests that a valid url can be accessed normally
        """
        response = request_session('https://example.com', 'GET')
        self.assertTrue(response.status_code, 200)

    def test_request_session_bad_url(self):
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

    @patch('kaznet.apps.ona.api.Retry._sleep_backoff')
    def test_request_session_retry(self, mocked):
        """
        Test that retry is attempted the given number of times
        """
        # Mocking Retry._sleep_backoff due to the fact
        # That it is one of the methods called per Retry
        # pylint: disable=protected-access
        mocked.side_effect = Retry._sleep_backoff()

        with self.assertRaises(RetryError):
            request_session(
                url='http://httpbin.org/status/504',
                method='GET',
                retries=2,
                backoff_factor=0
                )

        # We assert it's 3 since _sleep_backoff is called
        # first on Initialization Then repeated each Retry
        self.assertEqual(mocked.call_count, 3)

    def test_get_project_obj(self):
        """
        Test that get_project_obj returns correct Project Object
        """
        mocked_project = mommy.make('ona.Project', ona_pk=999)
        project = get_project_obj(ona_project_id=999)

        self.assertEqual(mocked_project, project)

    def test_get_xfrom_obj(self):
        """
        Test that get_xform_obj returns correct XForm Object
        """
        mocked_xform = mommy.make('ona.XForm', ona_pk=876)
        project = get_xform_obj(876)

        self.assertTrue(mocked_xform, project)
