"""
Module containing tests for
Ona Apps api.py methods
"""

from unittest.mock import patch
from urllib.parse import urljoin

from django.test import TestCase, override_settings

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
from django.conf import settings


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

    @override_settings(
        ONA_BASE_URL='https://stage-api.ona.io', ONA_USERNAME='kaznettest')
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
            urljoin(settings.ONA_BASE_URL, 'api/v1/projects?owner=kaznettest'),
            json=mocked_projects_data
            )
        response = get_projects(username=settings.ONA_USERNAME)

        self.assertEqual(response, mocked_projects_data)

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
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
            urljoin(
                settings.ONA_BASE_URL, '/api/v1/data/53?start=0&limit=100'),
            json=mocked_instances
        )
        mocked.get(
            urljoin(
                settings.ONA_BASE_URL, '/api/v1/data/53?start=100&limit=100'),
            json=[]
        )

        response = get_instances(53)
        for i in response:
            mocked_data = i
        self.assertEqual(mocked_data, mocked_instances)

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
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

        url = urljoin(settings.ONA_BASE_URL, 'api/v1/projects/18')
        mocked.get(
            url,
            json=mocked_project_data
            )
        response = get_project(url)

        self.assertTrue(response, mocked_project_data)

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
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

        url = urljoin(settings.ONA_BASE_URL, 'api/v1/forms/53')
        mocked.get(
            url,
            json=mocked_xform_data
            )
        response = get_xform(53)

        self.assertTrue(response, mocked_xform_data)

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
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

        url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53/142')
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

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
    @requests_mock.Mocker()
    def test_process_xform_good_data(self, mocked):
        """
        Test that when process_xform is called with valid data
        it creates an XForm Object and a Project Object
        If its not present
        """
        # Creates Project if not present
        mocked_form_data = {
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False,
            "date_modified": "2018-02-15T07:51:59.267839Z"
        }

        mocked_project_data = {
            "projectid": 18,
            "name": "Changed2",
            "date_modified": "2018-05-30T07:51:59.267839Z",
            "deleted_at": None
        }

        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/projects/18'),
            json=mocked_project_data
        )

        self.assertEqual(XForm.objects.all().count(), 0)
        self.assertEqual(Project.objects.all().count(), 0)
        process_xform(mocked_form_data, 18)

        self.assertEqual(XForm.objects.all().count(), 1)
        self.assertEqual(Project.objects.all().count(), 1)

        the_xform = XForm.objects.first()

        self.assertEqual("aFEjJKzULJbQYsmQzKcpL9", the_xform.id_string)
        self.assertEqual("Changed", the_xform.title)
        self.assertEqual(18, the_xform.project_id)
        self.assertEqual(53, the_xform.ona_pk)

        # Doesnt create a project if present

        mommy.make('ona.Project', ona_pk=49)

        mocked_form_data = {
            "name": "Salaries",
            "formid": 90,
            "id_string": "aFEjJKzULJlQYsmQzKcpL9",
            "is_merged_dataset": False,
            "date_modified": "2018-02-15T07:51:59.267839Z"
        }

        self.assertEqual(XForm.objects.all().count(), 1)
        self.assertEqual(Project.objects.all().count(), 2)
        process_xform(mocked_form_data, 49)

        self.assertEqual(XForm.objects.all().count(), 2)
        self.assertEqual(Project.objects.all().count(), 2)

        # Doesn't Create an XForm if already Present

        mocked_form_data = {
            "name": "Salaries",
            "formid": 90,
            "id_string": "aFEjJKzULJlQYsmQzKcpL9",
            "is_merged_dataset": False,
            "date_modified": "2018-02-15T07:51:59.267839Z",
        }

        self.assertEqual(XForm.objects.all().count(), 2)
        self.assertEqual(Project.objects.all().count(), 2)
        process_xform(mocked_form_data, 49)

        self.assertEqual(XForm.objects.all().count(), 2)
        self.assertEqual(Project.objects.all().count(), 2)

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

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
    @requests_mock.Mocker()
    def test_process_instance_good_data(self, mocked):
        """
        Test that when process_instance is called with valid data
        it creates an Instance Object as well as an XForm object and a Project
        Object if not present.
        """
        # Creates XForm and Project if Missing
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
            urljoin(settings.ONA_BASE_URL, '/api/v1/projects/18'),
            json=mocked_project_data
        )

        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/projects/20'),
            json=mocked_project_data
        )

        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/53'),
            json=mocked_form_data
        )
        self.assertEqual(Instance.objects.all().count(), 0)
        self.assertEqual(XForm.objects.all().count(), 0)
        self.assertEqual(Project.objects.all().count(), 0)

        process_instance(mocked_instance_data)

        self.assertEqual(Instance.objects.all().count(), 1)
        self.assertEqual(XForm.objects.all().count(), 1)
        self.assertEqual(Project.objects.all().count(), 1)

        # Doesn't Create a Project if its already there

        mommy.make('ona.Project', ona_pk=20)

        mocked_instance_data = {
            "_xform_id_string": "aFEjJKzPLJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-05-30T07:51:59.187363Z",
            "_xform_id": 52,
            "_submitted_by": "sluggie",
            "_id": 1785
        }

        mocked_form_data = {
            "name": "Changed",
            "formid": 52,
            "id_string": "aFEjJKzPLJbQYsmQzKcpL9",
            "is_merged_dataset": False,
            "project": "https://stage-api.ona.io/api/v1/projects/20"
        }

        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/52'),
            json=mocked_form_data
        )

        self.assertEqual(Instance.objects.all().count(), 1)
        self.assertEqual(XForm.objects.all().count(), 1)
        self.assertEqual(Project.objects.all().count(), 2)

        process_instance(mocked_instance_data)

        self.assertEqual(Instance.objects.all().count(), 2)
        self.assertEqual(XForm.objects.all().count(), 2)
        self.assertEqual(Project.objects.all().count(), 2)

        # Doesn't create an XForm or Project if both are present

        mocked_instance_data = {
            "_xform_id_string": "aFEjJKzSLJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-05-30T07:51:59.187363Z",
            "_xform_id": 25,
            "_submitted_by": "sluggie",
            "_id": 1759
        }

        mommy.make('ona.Project', ona_pk=49)
        mommy.make('ona.XForm', ona_pk=25, project_id=49)

        self.assertEqual(Instance.objects.all().count(), 2)
        self.assertEqual(XForm.objects.all().count(), 3)
        self.assertEqual(Project.objects.all().count(), 3)

        process_instance(mocked_instance_data)

        self.assertEqual(Instance.objects.all().count(), 3)
        self.assertEqual(XForm.objects.all().count(), 3)
        self.assertEqual(Project.objects.all().count(), 3)

        # Doesn't create an Instance if its Already Present
        mocked_instance_data = {
            "_xform_id_string": "aFEjJKzSLJbQYsmQzKcpL9",
            "_edited": True,
            "_last_edited": "2018-06-01T07:51:59.187363Z",
            "_xform_id": 25,
            "_submitted_by": "sluggie",
            "_id": 1759
        }

        self.assertEqual(Instance.objects.all().count(), 3)
        self.assertEqual(XForm.objects.all().count(), 3)
        self.assertEqual(Project.objects.all().count(), 3)

        process_instance(mocked_instance_data)

        self.assertEqual(Instance.objects.all().count(), 3)
        self.assertEqual(XForm.objects.all().count(), 3)
        self.assertEqual(Project.objects.all().count(), 3)

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

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
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
        url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53')
        mocked.get(
            url,
            json=mocked_response
            )
        response = request(url)

        self.assertEqual(mocked_response, response)

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
    @requests_mock.Mocker()
    def test_request_bad_data(self, mocked):
        """
        Test that request returns None for Incorrect Data
        """
        url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53')
        mocked.get(
            url,
            text='Oh! Hello There!'
            )
        response = request(url)

        self.assertEqual(response, None)

        # Request returns None for requests that aren't GET or POST

        url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53')
        response = request(url, method='PUT')

        self.assertEqual(response, None)

    def test_request_session(self):
        """
        Tests that request_session works the way it should
        """
        response = request_session('https://example.com', 'GET')
        self.assertEqual(response.status_code, 200)

        # Returns None for request methods that aren't GET or POST

        response = request_session('https://example.com', 'PUT')
        self.assertEqual(response, None)

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

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
    @requests_mock.Mocker()
    def test_get_project_obj(self, mocked):
        """
        Test that get_project_obj returns correct Project Object
        """
        # Can retrieve project object by use of id
        mocked_project = mommy.make('ona.Project', ona_pk=999)
        project = get_project_obj(ona_project_id=999)

        self.assertEqual(mocked_project, project)

        # Creates Project if not in system

        mocked_project_data = {
            "projectid": 3,
            "name": "Solo",
            "date_modified": "2018-05-30T07:51:59.267839Z",
            "deleted_at": None
        }

        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/projects/3'),
            json=mocked_project_data
        )
        self.assertEqual(Project.objects.all().count(), 1)
        project = get_project_obj(ona_project_id=3)

        self.assertEqual(Project.objects.all().count(), 2)
        self.assertEqual(project.name, 'Solo')

        # Returns correct project when given a url

        mocked_project_data = {
            "projectid": 3,
            "name": "Solo",
            "date_modified": "2018-05-30T07:51:59.267839Z",
            "deleted_at": None
        }
        url = urljoin(settings.ONA_BASE_URL, '/api/v1/projects/3')
        mocked.get(
            url,
            json=mocked_project_data
        )
        self.assertEqual(Project.objects.all().count(), 2)
        mocked_project = get_project_obj(project_url=url)

        self.assertEqual(Project.objects.all().count(), 2)
        self.assertEqual(project, mocked_project)

    def test_get_xfrom_obj(self):
        """
        Test that get_xform_obj returns correct XForm Object
        """
        mocked_xform = mommy.make('ona.XForm', ona_pk=876)
        project = get_xform_obj(876)

        self.assertTrue(mocked_xform, project)
