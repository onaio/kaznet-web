"""
Module containing tests for
Ona Apps api.py methods
"""
from unittest.mock import patch
from urllib.parse import urljoin

import requests_mock
from django.conf import settings
from django.test import override_settings
from django.utils import timezone
from model_mommy import mommy
from requests.exceptions import RetryError
# pylint: disable=import-error
from requests.packages.urllib3.util.retry import Retry

from kaznet.apps.main.common_tags import (FILTERED_DATASETS_FIELD_NAME,
                                          HAS_FILTERED_DATASETS_FIELD_NAME,
                                          HAS_WEBHOOK_FIELD_NAME,
                                          WEBHOOK_FIELD_NAME)
from kaznet.apps.main.models import Task
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.api import (create_filtered_data_sets,
                                 create_filtered_dataset, create_form_webhook,
                                 delete_filtered_dataset, fetch_form_data,
                                 fetch_missing_instances,
                                 get_and_process_xforms, get_project,
                                 get_project_obj, get_projects, get_xform,
                                 get_xform_obj, process_instance,
                                 process_project, process_projects,
                                 process_xform, process_xforms, request,
                                 request_session, sync_deleted_instances,
                                 sync_deleted_projects, sync_deleted_xforms,
                                 sync_updated_instances,
                                 update_user_profile_metadata)
from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.apps.users.models import UserProfile

# pylint: disable=bad-continuation
MOCKED_ONA_FORM_DATA = {
    'name': 'constraint_example', 'title': 'Constraint Form',
    'sms_keyword': 'constraint_example', 'default_language': 'default',
    'version': '201810090735', 'id_string': 'constraint_example',
    'type': 'survey', 'children': [
        {'bind': {'jr:constraintMsg': 'Requires a number less than 10',
                  'constraint': '. < 10'}, 'label': 'Integer', 'type': 'int',
         'name': 'my_int', 'hint': 'Try entering a number < 10'},
        {'bind': {
            'jr:constraintMsg': 'Requires a number between 10.51 and 18.39',
            'constraint': '. > 10.51 and . < 18.39'}, 'label': 'Decimal',
            'type': 'decimal', 'name': 'my_decimal',
                    'hint': 'Only numbers > 10.51 and < 18.39'},
        {'bind': {
            'jr:constraintMsg': 'Requires a date that is not before today',
            'constraint': '. >= today()'}, 'label': 'Date', 'type': 'date',
            'name': 'my_date', 'hint': 'Only future dates allowed'},
        {'control': {'bodyless': True},
         'type': 'group',
         'children': [
             {'bind': {
                'readonly': 'true()', 'calculate': "concat('uuid:', uuid())"},
                 'type': 'calculate', 'name': 'instanceID'}],
         'name': 'meta'}]}


# pylint: disable=too-many-public-methods
class TestApiMethods(MainTestBase):
    """
    Tests for the API Methods
    """

    def setUp(self):
        super().setUp()
        self.user = mommy.make('auth.User', username='sluggie')

    @override_settings(
        ONA_BASE_URL='https://stage-api.ona.io', ONA_USERNAME='kaznettest')
    @requests_mock.Mocker()
    def test_get_projects(self, mocked):
        """
        Test to see that get_projects returns the
        correct data
        """
        mocked_projects_data = [{
            "projectid": 18,
            "forms": [{
                "name": "Changed",
                "formid": 53,
                "id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "is_merged_dataset": False,
                "version": "vQZYoAo96pzTHZHY2iWuQA",
                "owner": "https://example.com/api/v1/users/kaznet",
            }],
            "name":
            "Changed2",
            "date_modified":
            "2018-05-30T07:51:59.267839Z",
            "deleted_at":
            None
        }]

        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/projects?owner=kaznettest'),
            json=mocked_projects_data)
        response = get_projects(username=settings.ONA_USERNAME)

        self.assertEqual(response, mocked_projects_data)

    @override_settings(
        ONA_BASE_URL='https://stage-api.ona.io', ONA_USERNAME='kaznettest')
    @requests_mock.Mocker()
    def test_sync_deleted_projects(self, mocked):
        """
        Test sync_deleted_projects
        """
        Project.objects.all().delete()
        proj = mommy.make('ona.Project', ona_pk=1337)

        # make 3 more projects
        mommy.make('ona.Project', _quantity=3)

        # make some forms
        proj_with_submissions = mommy.make('ona.Project')
        xform = mommy.make('ona.XForm', ona_project_id=1337,
                           project=proj_with_submissions)

        xform_id = xform.id
        deleted_projects = Project.objects.exclude(
            id=proj.id).values_list('id', flat=True)

        # make some instances
        mommy.make('ona.Instance', _quantity=13, xform=xform)
        instance = mommy.make('ona.Instance', xform=xform)

        # make some submissions
        task = mommy.make('main.Task', name='Cattle Price')

        mommy.make(
            'main.Submission',
            task=task,
            target_content_object=instance,
            _quantity=70,
            _fill_optional=['user', 'comment', 'submission_time'])

        mocked_projects_data = [{
            "projectid": 1337,
            "forms": [{
                "name": "Changed",
                "formid": 53,
                "id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "is_merged_dataset": False,
                "version": "vQZYoAo96pzTHZHY2iWuQA",
                "owner": "https://example.com/api/v1/users/kaznet",
            }],
            "name":
            "Changed2",
            "date_modified":
            "2018-05-30T07:51:59.267839Z",
            "deleted_at":
            None
        }]

        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/projects?owner=kaznettest'),
            json=mocked_projects_data)
        sync_deleted_projects(username=settings.ONA_USERNAME)

        proj.refresh_from_db()
        self.assertEqual(1, Project.objects.count())
        self.assertEqual(proj, Project.objects.first())

        self.assertEqual(
            0, XForm.objects.filter(project__id__in=deleted_projects).count())
        self.assertEqual(
            0, Instance.objects.filter(xform__id=xform_id).count())

        task.refresh_from_db()
        self.assertEqual(Task.DRAFT, task.status)
        self.assertEqual(0, task.get_submissions())

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
        mocked.get(url, json=mocked_project_data)
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
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
            "is_merged_dataset": False
        }

        url = urljoin(settings.ONA_BASE_URL, 'api/v1/forms/53')
        mocked.get(url, json=mocked_xform_data)
        response = get_xform(53)

        self.assertTrue(response, mocked_xform_data)

    # pylint: disable=no-self-use
    @patch('kaznet.apps.ona.api.process_project')
    def test_process_projects(self, mockclass):
        """
        Test that process_projects works the way it
        should when given proper and improper data
        """
        mocked_projects_data = [{
            "projectid":
            18,
            "forms": [{
                "name": "Changed",
                "formid": 53,
                "version": "vQZYoAo96pzTHZHY2iWuQA",
                "owner": "https://example.com/api/v1/users/kaznet",
                "id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "is_merged_dataset": False
            }],
            "name":
            "Changed2",
            "date_modified":
            "2018-05-30T07:51:59.267839Z",
            "deleted_at":
            None
        }]

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
        mocked_forms_data = [{
            "name": "Changed",
            "formid": 53,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
            "is_merged_dataset": False
        }]

        # Test that when valid forms data is passed it calls process_xform
        process_xforms(mocked_forms_data, 18)
        mockclass.assert_called_with(mocked_forms_data[0], project_id=18)

        # Test that when invalid projects data is passed it does nothing
        mocked_forms_data = None

        process_xforms(mocked_forms_data, project_id=18)
        mockclass.assert_called_once()

    @patch('kaznet.apps.ona.api.process_xform')
    @patch('kaznet.apps.ona.api.get_xform')
    def test_get_and_process_xforms(self, get_xform_mock, process_xform_mock):
        """
        Test get_and_process_xforms
        """
        xform_data = {
            "name": "Form 66",
            "formid": 7331,
            "id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "is_merged_dataset": False,
            "version": "v5555555555",
            "owner": "https://example.com/api/v1/users/kaznet"
        }
        get_xform_mock.return_value = xform_data
        get_and_process_xforms([xform_data], 29)

        self.assertTrue(get_xform_mock.called)
        process_xform_mock.assert_called_with(
            xform_data, 29
        )

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
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
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
            json=mocked_project_data)
        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/53/form.json'),
            json=MOCKED_ONA_FORM_DATA
        )
        mocked.post(
            urljoin(settings.ONA_BASE_URL, 'api/v1/dataviews'),
            status_code=201
        )

        self.assertEqual(XForm.objects.all().count(), 0)
        self.assertEqual(Project.objects.all().count(), 0)
        process_xform(mocked_form_data, 18)

        self.assertEqual(XForm.objects.all().count(), 1)
        self.assertEqual(Project.objects.all().count(), 1)

        the_xform = XForm.objects.first()

        self.assertEqual("aFEjJKzULJbQYsmQzKcpL9", the_xform.id_string)
        self.assertEqual("Changed", the_xform.title)
        self.assertEqual("vQZYoAo96pzTHZHY2iWuQA", the_xform.version)
        self.assertEqual(
            "https://example.com/api/v1/users/kaznet",
            the_xform.json['owner_url']
        )
        self.assertEqual("kaznet", the_xform.json['owner'])
        self.assertEqual(18, the_xform.ona_project_id)
        self.assertEqual(53, the_xform.ona_pk)

        # Doesnt create a project if present

        mommy.make('ona.Project', ona_pk=49)

        mocked_form_data = {
            "name": "Salaries",
            "formid": 90,
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
            "id_string": "aFEjJKzULJlQYsmQzKcpL9",
            "is_merged_dataset": False,
            "date_modified": "2018-02-15T07:51:59.267839Z"
        }
        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/90/form.json'),
            json=MOCKED_ONA_FORM_DATA
        )

        self.assertEqual(XForm.objects.all().count(), 1)
        self.assertEqual(Project.objects.all().count(), 2)
        process_xform(mocked_form_data, 49)

        self.assertEqual(XForm.objects.all().count(), 2)
        self.assertEqual(Project.objects.all().count(), 2)

        # Doesn't Create an XForm if already Present

        mocked_form_data = {
            "name": "Salaries",
            "formid": 90,
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
            "id_string": "aFEjJKzULJlQYsmQzKcpL9",
            "is_merged_dataset": False,
            "date_modified": "2018-02-15T07:51:59.267839Z",
        }

        self.assertEqual(XForm.objects.all().count(), 2)
        self.assertEqual(Project.objects.all().count(), 2)
        process_xform(mocked_form_data, 49)

        self.assertEqual(XForm.objects.all().count(), 2)
        self.assertEqual(Project.objects.all().count(), 2)

    def test_process_xform_updates_fields(self):
        """
        Test that certain fields are always updated if different
        """
        the_xform = mommy.make(
            'ona.XForm',
            title="First Title",
            version="v1",
            json={
                "owner": "1",
                "owner_url": "http://example.com/1",
            },
            ona_pk=1337,
            last_updated="2018-02-15T07:51:59.267839Z"
        )

        mocked_form_data = {
            "title": "Big Form",
            "formid": 1337,
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
            "id_string": "aFEjJKzULJlQYsmQzKcpL9",
            "is_merged_dataset": False,
            "date_modified": "2018-02-15T07:51:59.267839Z",
            "last_updated_at": "2018-02-15T07:55:59.267839Z",
        }

        process_xform(mocked_form_data, mommy.make('ona.Project').ona_pk)

        the_xform.refresh_from_db()

        self.assertEqual("Big Form", the_xform.title)
        self.assertEqual("vQZYoAo96pzTHZHY2iWuQA", the_xform.version)
        self.assertEqual("kaznet", the_xform.json['owner'])
        self.assertEqual(
            "2018-02-15T07:55:59.267839+00:00",
            the_xform.last_updated.isoformat())
        self.assertEqual(
            "https://example.com/api/v1/users/kaznet",
            the_xform.json['owner_url'])

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
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
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
            json=mocked_project_data)

        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/projects/20'),
            json=mocked_project_data)

        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/53'),
            json=mocked_form_data)
        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/53/form.json'),
            json=MOCKED_ONA_FORM_DATA
        )
        mocked.post(
            urljoin(settings.ONA_BASE_URL, 'api/v1/dataviews'),
            status_code=201
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
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
            "is_merged_dataset": False,
            "project": "https://stage-api.ona.io/api/v1/projects/20"
        }

        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/52'),
            json=mocked_form_data)
        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/52/form.json'),
            json=MOCKED_ONA_FORM_DATA
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
        mocked.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/25/form.json'),
            json=MOCKED_ONA_FORM_DATA
        )

        mommy.make('ona.Project', ona_pk=49)
        mommy.make('ona.XForm', ona_pk=25, ona_project_id=49)

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
            "version": "vQZYoAo96pzTHZHY2iWuQA",
            "owner": "https://example.com/api/v1/users/kaznet",
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
        mocked_response = [{
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": False,
            "_last_edited": "2018-05-30T07:51:59.187363+00:00",
            "_xform_id": 53,
            "_id": 1755
        }]
        url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53')
        mocked.get(url, json=mocked_response)
        response = request(url)

        self.assertEqual(mocked_response, response)

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
    @requests_mock.Mocker()
    def test_request_bad_data(self, mocked):
        """
        Test that request returns None for Incorrect Data
        """
        url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53')
        mocked.get(url, text='Oh! Hello There!')
        response = request(url)

        self.assertEqual(response, None)

    def test_request_session_bad_url(self):
        """
        Test that an invalid url will fail eventually
        """

        with self.assertRaises(RetryError):
            request_session(
                url='http://httpbin.org/status/500',
                method='GET',
                retries=3,
                backoff_factor=0)

        with self.assertRaises(RetryError):
            request_session(
                url='http://httpbin.org/status/502',
                method='GET',
                retries=3,
                backoff_factor=0)

        with self.assertRaises(RetryError):
            request_session(
                url='http://httpbin.org/status/504',
                method='GET',
                retries=3,
                backoff_factor=0)

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
                backoff_factor=0)

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
            json=mocked_project_data)
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
        mocked.get(url, json=mocked_project_data)
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

    @override_settings(ONA_BASE_URL='https://stage-api.ona.io')
    @requests_mock.Mocker()
    def test_create_form_webhook(self, mocked):
        """
        Test create_form_webhook
        """
        xform = mommy.make(
            'ona.XForm', title="Red Dead Redemption", ona_pk=888999)
        mocked_restservice = {
            'id': 777,
            'xform': xform.ona_pk,
            'name': 'TEST',
            'service_url': 'http://example.com',
            'active': True,
            'inactive_reason': ''
        }

        mocked.post(
            url=f'{settings.ONA_BASE_URL}/api/v1/restservices',
            json=mocked_restservice,
            status_code=201)

        response = create_form_webhook(
            form_id=xform.ona_pk,
            service_url='http://example.com',
            name='TEST')
        self.assertDictEqual(mocked_restservice, response.json())
        self.assertEqual(201, response.status_code)

        xform.refresh_from_db()
        self.assertTrue(xform.json[HAS_WEBHOOK_FIELD_NAME])
        self.assertTrue(mocked_restservice in xform.json[WEBHOOK_FIELD_NAME])
        self.assertEqual(1, len(xform.json[WEBHOOK_FIELD_NAME]))

    @requests_mock.Mocker()
    @patch('kaznet.apps.ona.api.cache')
    def test_update_user_profile_metadata(self, mocked, mocked_cache):
        """
        Test that update_user_profile_metadata updates
        with correct data
        """
        support_user = mommy.make(
            'auth.User', username='onasupport')
        profile = support_user.userprofile
        profile.ona_username = 'bob'
        profile.save()

        mocked_user_profile_data = {
            'id': self.user.pk,
            'url': 'http://testserver/api/v1/profiles/bob',
            'username': 'bob',
            'first_name': 'Bob',
            'last_name': 'erama',
            'email': 'bob@columbia.edu',
            'city': 'Bobville',
            'country': 'US',
            'organization': 'Bob Inc.',
            'website': 'bob.com',
            'twitter': 'boberama',
            'require_auth': False,
            'user': 'http://testserver/api/v1/users/bob',
            'is_org': False,
            'gravatar': 'https://somelink.com/me.png',
            'metadata': {
                'last_password_edit': timezone.now().isoformat()
            },
            'joined_on': self.user.date_joined.isoformat(),
            'name': 'Bob erama'
        }

        mocked_cache.get.return_value = 'token'
        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/profiles/bob/'),
            json=mocked_user_profile_data)

        update_user_profile_metadata(ona_username='bob')

        # pylint: disable=no-member
        profile = UserProfile.objects.get(ona_username='bob')

        self.assertEqual(
            mocked_user_profile_data['metadata']['last_password_edit'],
            profile.metadata['last_password_edit'])
        self.assertEqual(
            mocked_user_profile_data['gravatar'],
            profile.metadata['gravatar'])

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_create_filtered_dataset(self, mocked):
        """
        Test create_filtered_dataset
        """
        xform = mommy.make(
            'ona.XForm', title="Red Dead Redemption", ona_pk=349451,
            ona_project_id=64730)

        mocked_dataview = {
            'dataviewid': 708473,
            'name': 'Red Dead Redemption - test',
            'xform': 'https://mosh-ona.io/api/v1/forms/349451',
            'project': 'https://mosh-ona.io/api/v1/projects/64730',
            'columns': [
                '_review_status',
                '_review_comment',
                'instanceID',
                '_last_edited',
                '_submitted_by',
                '_media_all_received',
                'resp_name',
                'resp_age',
                'live',
                'rate',
                'rate_label',
                'feel',
                'meta'
            ],
            'query': [
                {
                    'column': '_review_status',
                    'filter': '=',
                    'condition': 'or',
                    'value': '1'
                }
            ],
            'matches_parent': False,
            'count': 0,
            'instances_with_geopoints': False,
            'last_submission_time': None,
            'has_hxl_support': False,
            'url': 'https://mosh-ona.io/api/v1/dataviews/708473',
            'date_created': '2018-11-08T03:41:47.495132-05:00',
            'deleted_at': None,
            'deleted_by': None
        }

        payload = {
            'xform': 'https://api.ona.io/api/v1/forms/349451',
            'project': 'https://api.ona.io/api/v1/projects/64730',
            'columns': [
                '_review_status',
                '_review_comment',
                'instanceID',
                '_last_edited',
                '_submitted_by',
                '_media_all_received',
                'resp_name',
                'resp_age',
                'live',
                'rate',
                'rate_label',
                'feel',
                'meta'
            ],
            'name': 'Red Dead Redemption - test',
            'query': [
                {
                    'column': '_review_status',
                    'filter': '=',
                    'value': '1',
                    'condition': 'or'
                }
            ]
        }

        mocked.post(
            url=f'{settings.ONA_BASE_URL}/api/v1/dataviews',
            json=mocked_dataview,
            status_code=201)

        response = create_filtered_dataset(
            form_id=xform.ona_pk,
            payload=payload
        )

        self.assertTrue(mocked.called)
        self.assertDictEqual(payload, mocked.last_request.json())

        self.assertDictEqual(mocked_dataview, response.json())
        self.assertEqual(201, response.status_code)

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_delete_filtered_dataset(self, mocked):
        """
        Test delete_filtered_dataset
        """
        xform = mommy.make(
            'ona.XForm', title="Red Dead Redemption", ona_pk=349452,
            ona_project_id=64731)

        dataset_url = f'{settings.ONA_BASE_URL}/api/v1/dataviews/1'

        mocked.delete(
            url=dataset_url,
            text='',
            status_code=204)

        response = delete_filtered_dataset(
            form_id=xform.ona_pk, dataset_url=dataset_url)

        self.assertEqual('mosh-ona.io', mocked.last_request.hostname)
        self.assertEqual('/api/v1/dataviews/1', mocked.last_request.path)
        self.assertEqual(204, response.status_code)

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_create_filtered_data_sets(self, mocked):
        """
        Test create_filtered_data_sets
        """
        xform = mommy.make(
            'ona.XForm', title="Coconut", ona_pk=349455,
            ona_project_id=64735)

        mocked_form = {
            "name": "attachment_test",
            "title": "attachment_test",
            "sms_keyword": "attachment_test",
            "default_language": "default",
            "version": "201710300941",
            "id_string": "attachment_test",
            "type": "survey",
            "children": [{
                "type": "text",
                "name": "name",
                "label": "Name"
            }, {
                "type": "photo",
                "name": "image1",
                "label": "Photo"
            }, {
                "control": {
                    "bodyless": True
                },
                "type": "group",
                "children": [{
                    "bind": {
                        "readonly": "true()",
                        "calculate": "concat('uuid:', uuid())"
                    },
                    "type": "calculate",
                    "name": "instanceID"
                }],
                "name": "meta"
            }]
        }

        mocked_dataview = {
            'dataviewid': 708477,
            'name': 'Coconut - test',
            'xform': 'https://mosh-ona.io/api/v1/forms/349455',
            'project': 'https://mosh-ona.io/api/v1/projects/64735',
            'columns': [
                '_review_status',
                '_review_comment',
                'instanceID',
                '_last_edited',
                '_submitted_by',
                '_media_all_received',
                'name',
                'image1',
                'meta'
            ],
            'query': [
                {
                    'column': '_review_status',
                    'filter': '=',
                    'condition': 'or',
                    'value': '1'
                }
            ],
            'matches_parent': False,
            'count': 0,
            'instances_with_geopoints': False,
            'last_submission_time': None,
            'has_hxl_support': False,
            'url': 'https://mosh-ona.io/api/v1/dataviews/708477',
            'date_created': '2018-11-08T03:41:47.495132-05:00',
            'deleted_at': None,
            'deleted_by': None
        }

        last_payload = {
            'xform': 'https://mosh-ona.io/api/v1/forms/349455',
            'project': 'https://mosh-ona.io/api/v1/projects/64735',
            'columns': [
                '_review_status',
                '_review_comment',
                'instanceID',
                '_last_edited',
                '_submitted_by',
                '_media_all_received',
                'name',
                'image1',
                'meta'
            ],
            'name': 'Coconut - Pending Review',
            'query': [
                {
                    'column': '_review_status',
                    'filter': '=',
                    'value': '3',
                    'condition': 'or'
                }
            ]
        }

        mocked.post(
            url=f'{settings.ONA_BASE_URL}/api/v1/dataviews',
            json=mocked_dataview,
            status_code=201)

        mocked.get(
            url=f'{settings.ONA_BASE_URL}/api/v1/forms/349455/form.json',
            json=mocked_form,
            status_code=200
        )

        create_filtered_data_sets(
            form_id=xform.ona_pk,
            project_id=xform.ona_project_id,
            form_title="Coconut")

        self.assertEqual(4, mocked.call_count)
        self.assertDictEqual(last_payload, mocked.last_request.json())

        xform.refresh_from_db()
        self.assertTrue(xform.json[HAS_FILTERED_DATASETS_FIELD_NAME])
        self.assertEqual(
            [mocked_dataview, mocked_dataview, mocked_dataview],
            xform.json[FILTERED_DATASETS_FIELD_NAME])
        self.assertEqual(3, len(xform.json[FILTERED_DATASETS_FIELD_NAME]))

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_create_filtered_data_sets_failure(self, mocked):
        """
        Test create_filtered_data_sets where at least one dataset is not
        created successfully
        """
        xform = mommy.make(
            'ona.XForm', title="Attachment Test", ona_pk=666,
            ona_project_id=777)

        mocked_form = {
            "name": "attachment_test",
            "title": "attachment_test",
            "sms_keyword": "attachment_test",
            "default_language": "default",
            "version": "201710300941",
            "id_string": "attachment_test",
            "type": "survey",
            "children": [{
                "type": "text",
                "name": "name",
                "label": "Name"
            }, {
                "type": "photo",
                "name": "image1",
                "label": "Photo"
            }, {
                "control": {
                    "bodyless": True
                },
                "type": "group",
                "children": [{
                    "bind": {
                        "readonly": "true()",
                        "calculate": "concat('uuid:', uuid())"
                    },
                    "type": "calculate",
                    "name": "instanceID"
                }],
                "name": "meta"
            }]
        }

        mocked_dataview = {
            'dataviewid': 101010,
            'url': 'https://mosh-ona.io/api/v1/dataviews/101010',
        }

        # make it such that we only create one dataset successfully
        mocked.register_uri(
            'POST',
            f'{settings.ONA_BASE_URL}/api/v1/dataviews',
            [
                {'json': mocked_dataview, 'status_code': 201},
                {'text': 'catastrophic error!', 'status_code': 500}
            ]
        )

        mocked.get(
            url=f'{settings.ONA_BASE_URL}/api/v1/forms/666/form.json',
            json=mocked_form,
            status_code=200
        )

        mocked.delete(
            url=f'{settings.ONA_BASE_URL}/api/v1/dataviews/101010',
            text='',
            status_code=204
        )

        create_filtered_data_sets(
            form_id=xform.ona_pk,
            project_id=xform.ona_project_id,
            form_title="Attachment Test")

        self.assertEqual(5, mocked.call_count)
        self.assertEqual('mosh-ona.io', mocked.last_request.hostname)
        self.assertEqual('/api/v1/dataviews/101010', mocked.last_request.path)

        xform.refresh_from_db()
        self.assertFalse(xform.json[HAS_FILTERED_DATASETS_FIELD_NAME])
        self.assertEqual([], xform.json[FILTERED_DATASETS_FIELD_NAME])

    @patch('kaznet.apps.ona.api.Retry._sleep_backoff')
    def test_request_session_no_retries_404(self, mock):
        """
        Test how that 404s are not retried
        """
        request_session(
            url='http://httpbin.org/status/404',
            method='GET',
            retries=2,
            backoff_factor=0)
        # no retries!!
        self.assertFalse(mock.called)

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_fetch_form_data(self, mocked):
        """
        Test fetch_form_data
        """
        mocked_response = [
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": False,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1755
            },
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": False,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1756
            },
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": False,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1757
            }
        ]
        mocked_single_submission_response = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": False,
            "_last_edited": "2018-05-30T07:51:59.187363+00:00",
            "_xform_id": 53,
            "_id": 1755
        }

        submissions_url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53.json')
        mocked.get(submissions_url, json=mocked_response)

        form_data = fetch_form_data(formid=53)
        self.assertEqual(form_data, mocked_response)
        self.assertTrue(mocked.called)
        # it was not called with any params
        self.assertEqual('', mocked.last_request.query)
        self.assertEqual(None, mocked.last_request.text)
        # called once
        self.assertEqual(1, mocked.call_count)

        single_submission_url = urljoin(
            settings.ONA_BASE_URL, 'api/v1/data/53/1755.json')
        mocked.get(single_submission_url,
                   json=mocked_single_submission_response)

        one_submission_data = fetch_form_data(formid=53, dataid=1755)
        self.assertDictEqual(
            one_submission_data, mocked_single_submission_response)
        self.assertTrue(mocked.called)
        # it was again not called with any params
        self.assertEqual('', mocked.last_request.query)
        self.assertEqual(None, mocked.last_request.text)
        # now called twice
        self.assertEqual(2, mocked.call_count)

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_fetch_form_data_dataids_only(self, mocked):
        """
        Test fetch_form_data
        """
        mocked_response = [
            {"_id": 24873628},
            {"_id": 24873620},
            {"_id": 24873235},
            {"_id": 24873232},
            {"_id": 18179780},
            {"_id": 18179451},
            {"_id": 18179438}
        ]

        submissions_url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53.json')
        mocked.get(submissions_url, json=mocked_response)

        form_data = fetch_form_data(formid=53, dataids_only=True)
        self.assertEqual(form_data, mocked_response)
        self.assertTrue(mocked.called)
        # it was not called with any params
        self.assertEqual('fields=%5b%22_id%22%5d', mocked.last_request.query)
        # nothing in the request body
        self.assertEqual(None, mocked.last_request.text)
        # called once
        self.assertEqual(1, mocked.call_count)

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_fetch_form_data_edited_only(self, mocked):
        """
        Test fetch_form_data
        """
        mocked_response = [
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": False,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1755
            },
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": False,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1756
            }
        ]

        submissions_url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53.json')
        mocked.get(submissions_url, json=mocked_response)

        form_data = fetch_form_data(formid=53, edited_only=True)
        self.assertEqual(form_data, mocked_response)
        self.assertTrue(mocked.called)
        # it was not called with any params
        self.assertEqual('query=%7b%22_edited%22%3a%22true%22%7d',
                         mocked.last_request.query)
        # nothing in the request body
        self.assertEqual(None, mocked.last_request.text)
        # called once
        self.assertEqual(1, mocked.call_count)

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_fetch_form_data_latest(self, mocked):
        """
        Test fetch_form_data
        """
        mocked_response = [
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": False,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1755
            },
            {
                "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "_edited": False,
                "_last_edited": "2018-05-30T07:51:59.187363+00:00",
                "_xform_id": 53,
                "_id": 1756
            }
        ]

        submissions_url = urljoin(settings.ONA_BASE_URL, 'api/v1/data/53.json')
        mocked.get(submissions_url, json=mocked_response)

        form_data = fetch_form_data(formid=53, latest=1754)
        self.assertEqual(form_data, mocked_response)
        self.assertTrue(mocked.called)
        # it was not called with any params
        self.assertEqual(
            'query=%7b%22_id%22%3a%7b%22%24gte%22%3a1754%7d%7d',
            mocked.last_request.query)
        # nothing in the request body
        self.assertEqual(None, mocked.last_request.text)
        # called once
        self.assertEqual(1, mocked.call_count)

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    @patch('kaznet.apps.ona.api.process_instance')
    def test_fetch_missing_instances(
            self, mocked_request, mocked_process_instance):
        """
        Test fetch_missing_instances
        """
        xform = mommy.make('ona.XForm', title="fetch_missing_instances Test")
        mocked_ids_response = [
            {"_id": 1755}
        ]
        mocked_record_response = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": False,
            "_last_edited": "2018-05-30T07:51:59.187363+00:00",
            "_xform_id": xform.ona_pk,
            "_id": 1755
        }
        raw_ids_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{xform.ona_pk}.json')
        mocked_request.get(raw_ids_url, json=mocked_ids_response)

        record_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{xform.ona_pk}/1755.json')
        mocked_request.get(record_url, json=mocked_record_response)

        fetch_missing_instances(form_id=xform.ona_pk)

        self.assertEqual(2, mocked_request.call_count)
        self.assertEqual(1, mocked_process_instance.call_count)
        mocked_process_instance.assert_called_with(
            instance_data=mocked_record_response, xform=xform
        )

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    @patch('kaznet.apps.ona.api.process_instance')
    def test_sync_updated_instances(
            self, mocked_request, mocked_process_instance):
        """
        Test sync_updated_instances
        """
        xform = mommy.make('ona.XForm', title="sync_updated_instances Test")
        mocked_ids_response = [
            {"_id": 155}
        ]
        mocked_record_response = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": False,
            "_last_edited": "2018-05-30T07:51:59.187363+00:00",
            "_xform_id": xform.ona_pk,
            "_id": 155
        }
        raw_ids_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{xform.ona_pk}.json')
        mocked_request.get(raw_ids_url, json=mocked_ids_response)

        record_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{xform.ona_pk}/155.json')
        mocked_request.get(record_url, json=mocked_record_response)

        sync_updated_instances(form_id=xform.ona_pk)

        self.assertEqual(2, mocked_request.call_count)
        self.assertEqual(1, mocked_process_instance.call_count)
        mocked_process_instance.assert_called_with(
            instance_data=mocked_record_response, xform=xform
        )

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    @patch('kaznet.apps.ona.api.process_instance')
    def test_fetch_missing_instances_with_existing(
            self, mocked_request, mocked_process_instance):
        """
        Test fetch_missing_instances when we have existing records
        """
        xform = mommy.make('ona.XForm', title="fetch_missing_instances Test")
        mommy.make('ona.Instance', xform=xform, ona_pk=1755)
        mocked_ids_response = [
            {"_id": 1755}, {"_id": 1756}
        ]
        mocked_record_response = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": False,
            "_last_edited": "2018-05-30T07:51:59.187363+00:00",
            "_xform_id": xform.ona_pk,
            "_id": 1756
        }
        raw_ids_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{xform.ona_pk}.json')
        mocked_request.get(raw_ids_url, json=mocked_ids_response)

        record_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{xform.ona_pk}/1756.json')
        mocked_request.get(record_url, json=mocked_record_response)

        fetch_missing_instances(form_id=xform.ona_pk)

        self.assertEqual(2, mocked_request.call_count)
        self.assertEqual(1, mocked_process_instance.call_count)
        mocked_process_instance.assert_called_with(
            instance_data=mocked_record_response, xform=xform
        )

    @override_settings(
        ONA_BASE_URL='https://stage-api.ona.io', ONA_USERNAME='kaznettest')
    @requests_mock.Mocker()
    def test_sync_deleted_xforms(self, mocked):
        """
        Test sync_deleted_xforms
        """
        XForm.objects.all().delete()
        xform = mommy.make('ona.XForm', ona_pk=53)

        # make one more xform
        xform2 = mommy.make('ona.XForm', ona_pk=530798)

        # make some instances
        mommy.make('ona.Instance', _quantity=13, xform=xform)
        instance = mommy.make('ona.Instance', xform=xform)

        # make some submissions
        task = mommy.make('main.Task', name='Cattle Price')
        mommy.make(
            'main.Submission',
            task=task,
            target_content_object=instance,
            _quantity=70,
            _fill_optional=['user', 'comment', 'submission_time'])

        mocked_projects_data = [{
            "projectid": 1337,
            "forms": [
                {
                    "name": "Alive",
                    "formid": 530798,
                    "id_string": "iAmAlive",
                    "is_merged_dataset": False,
                    "version": "2",
                    "owner": "https://example.com/api/v1/users/kaznet",
                }
            ],
            "name":
            "Changed2",
            "date_modified":
            "2018-05-30T07:51:59.267839Z",
            "deleted_at":
            None
        }]

        mocked.get(
            urljoin(settings.ONA_BASE_URL, 'api/v1/projects?owner=kaznettest'),
            json=mocked_projects_data)

        sync_deleted_xforms(username=settings.ONA_USERNAME)

        self.assertFalse(XForm.objects.filter(id=xform.id).exists())
        self.assertFalse(Instance.objects.filter(xform__id=xform.id).exists())
        self.assertTrue(XForm.objects.filter(id=xform2.id).exists())
        task.refresh_from_db()
        self.assertEqual(Task.DRAFT, task.status)
        self.assertEqual(0, task.get_submissions())

    @override_settings(ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    def test_sync_deleted_instances(self, mocked_request):
        """
        Test sync_deleted_instances
        """
        Instance.objects.all().delete()
        xform = mommy.make('ona.XForm', title="sync_deleted_instances Test")
        mocked_ids_response = [
            {"_id": 159}
        ]
        raw_ids_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{xform.ona_pk}.json')
        mocked_request.get(raw_ids_url, json=mocked_ids_response)

        # make some instances
        instance1 = mommy.make('ona.Instance', xform=xform, ona_pk=155)
        instance2 = mommy.make('ona.Instance', xform=xform, ona_pk=159)

        # make some submissions
        task = mommy.make('main.Task', name='Cattle Price')
        mommy.make(
            'main.Submission',
            task=task,
            target_content_object=instance1,
            _quantity=70,
            _fill_optional=['user', 'comment', 'submission_time'])

        sync_deleted_instances(form_id=xform.ona_pk)

        self.assertFalse(Instance.objects.filter(id=instance1.id).exists())
        self.assertTrue(Instance.objects.filter(id=instance2.id).exists())
        task.refresh_from_db()
        self.assertEqual(0, task.get_submissions())
