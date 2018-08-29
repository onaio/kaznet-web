"""
Test module for celery tasks for Ona app
"""
from unittest.mock import call, patch

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone

import requests_mock
from model_mommy import mommy

from kaznet.apps.main.models import Task
from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.apps.ona.tasks import (
    task_fetch_all_instances, task_fetch_form_instances,
    task_fetch_project_xforms, task_fetch_projects, task_process_user_profiles)

MOCK_PROJECT_DATA = [
    {
        "projectid":
        1337,
        "forms": [
            {
                "name": "Form 66",
                "formid": 7331,
                "id_string": "aFEjJKzULJbQYsmQzKcpL9",
                "is_merged_dataset": False,
            },
            {
                "name": "Q-q-uest",
                "formid": 310,
                "id_string": "kjoin_zKcpL9",
                "is_merged_dataset": False,
            },
        ],
        "name":
        "Project of Life",
        "date_modified":
        "2018-05-30T07:51:59.267839Z",
        "deleted_at":
        None
    },
    {
        "projectid": 1333337,
        "forms": [],
        "name": "Hunter2",
        "date_modified": "2018-05-30T07:51:59.267839Z",
        "deleted_at": None
    },
]

MOCKED_INSTANCES = [
    {
        "_notes": [],
        "_media_all_received": True,
        "meta/instanceID": "uuid:b09078fe-9f8c-45dd-8119-09cbc97bb79f",
        "_attachments": [],
        "name": "BOBBBBBB",
        "_total_media": 0,
        "_xform_id": 253470,
        "_submission_time": "2017-10-30T09:50:38",
        "_uuid": "b09078fe-9f8c-45dd-8119-09cbc97bb79f",
        "_bamboo_dataset_id": "",
        "_tags": [],
        "_version": "201710300941",
        "_submitted_by": "onasupport",
        "_geolocation": [],
        "_edited": False,
        "_xform_id_string": "attachment_test",
        "_status": "submitted_via_web",
        "_id": 21311495,
        "_media_count": 0,
        "_duration": "",
    },
    {
        "_notes": [],
        "_media_all_received":
        True,
        "_bamboo_dataset_id":
        "",
        "_tags": [],
        "_xform_id_string":
        "attachment_test",
        "meta/instanceID":
        "uuid:65903eb7-6524-4f81-89df-5a3cc725910e",
        "_duration":
        "",
        "_geolocation": [None, None],
        "_edited":
        False,
        "_status":
        "submitted_via_web",
        "_uuid":
        "65903eb7-6524-4f81-89df-5a3cc725910e",
        "_submitted_by":
        "onasupport",
        "image1":
        "reece-12_48_29.JPG",
        "_media_count":
        1,
        "formhub/uuid":
        "fff2652efcd24709bb9236d24c77e918",
        "name":
        "ALLLIIICCCEE",
        "_total_media":
        1,
        "_xform_id":
        253470,
        "_submission_time":
        "2017-10-30T09:50:47",
        "_version":
        "201710300941",
        "_attachments": [],
        "_id":
        21311503
    },
]


class TestCeleryTasks(TestCase):
    """
    Tests for celery tasks
    """

    @override_settings(ONA_BASE_URL="https://example.com", ONA_USERNAME='mosh')
    @patch('kaznet.apps.ona.tasks.task_fetch_project_xforms.delay')
    @patch('kaznet.apps.ona.tasks.process_projects')
    @requests_mock.Mocker()
    def test_task_fetch_projects(self, mocked_process_projects,
                                 mocked_fetch_project_task, mocked_request):
        """
        Test task_fetch_projects
        """
        # mock the request
        mocked_request.get(
            "https://example.com/api/v1/projects?owner=mosh",
            json=MOCK_PROJECT_DATA)
        # run the task
        task_fetch_projects(username=settings.ONA_USERNAME)
        # we should call process_projects
        mocked_process_projects.assert_called_with(MOCK_PROJECT_DATA)
        # we should call task_fetch_project_xforms twice, for each form
        self.assertEqual(1, mocked_fetch_project_task.call_count)
        mocked_fetch_project_task.assert_called_with(
            forms=MOCK_PROJECT_DATA[0]['forms'],
            project_id=MOCK_PROJECT_DATA[0]['projectid'])

    @patch('kaznet.apps.ona.tasks.process_xforms')
    def test_task_fetch_project_xforms(self, mock):
        """
        Test task_fetch_project_xforms
        """
        # call the task
        task_fetch_project_xforms(MOCK_PROJECT_DATA[0]['forms'][1],
                                  MOCK_PROJECT_DATA[0]['projectid'])
        # we should have called process_xforms
        mock.assert_called_with(
            forms_data=MOCK_PROJECT_DATA[0]['forms'][1],
            project_id=MOCK_PROJECT_DATA[0]['projectid'])

    @override_settings(
        CELERY_TASK_ALWAYS_EAGER=True,
        ONA_BASE_URL="https://example.com",
        ONA_USERNAME='mosh')
    @requests_mock.Mocker()
    def test_fetch_projects_and_xforms(self, mocked_request):
        """
        Test that the `task_fetch_projects` task actually fetches and
        stores projects and XForms
        """
        # mock the request
        mocked_request.get(
            "https://example.com/api/v1/projects?owner=mosh",
            json=MOCK_PROJECT_DATA)
        # run the task
        task_fetch_projects(username=settings.ONA_USERNAME)
        # we should have two projects
        self.assertTrue(Project.objects.filter(ona_pk=1337).exists())
        self.assertTrue(Project.objects.filter(ona_pk=1333337).exists())
        # we should have two forms
        self.assertTrue(XForm.objects.filter(ona_pk=7331).exists())
        self.assertTrue(XForm.objects.filter(ona_pk=310).exists())

    @override_settings(ONA_BASE_URL="https://example.com")
    @patch('kaznet.apps.ona.tasks.process_instance')
    @requests_mock.Mocker()
    def test_task_fetch_form_instances(self, process_instance_mock,
                                       mocked_request):
        """
        Test task_fetch_form_instances
        """
        mommy.make('auth.User', username='onasupport')
        xform = mommy.make(
            'ona.XForm',
            id=7,
            ona_pk=897,
            id_string='attachment_test',
            title='attachment test')
        # mock the request
        mocked_request.get(
            "https://example.com/api/v1/data/897?start=0&limit=100",
            json=MOCKED_INSTANCES)
        mocked_request.get(
            "https://example.com/api/v1/data/897?start=100&limit=100", json=[])
        # call the task
        task_fetch_form_instances(xform_id=xform.id)
        # process_instance_mock should have been called twice
        self.assertEqual(2, process_instance_mock.call_count)

        expected_calls = [
            call(instance_data=MOCKED_INSTANCES[0], xform=xform),
            call(instance_data=MOCKED_INSTANCES[1], xform=xform)
        ]

        process_instance_mock.assert_has_calls(expected_calls)

    @override_settings(ONA_BASE_URL="https://example.com")
    @requests_mock.Mocker()
    def test_task_fetch_form_instances_integration(self, mocked_request):
        """
        Test task_fetch_form_instances results in actual instances
        """
        mommy.make('auth.User', username='onasupport')
        xform = mommy.make(
            'ona.XForm',
            id=7,
            ona_pk=897,
            id_string='attachment_test',
            title='attachment test')
        # mock the request
        mocked_request.get(
            "https://example.com/api/v1/data/897?start=0&limit=100",
            json=MOCKED_INSTANCES)
        mocked_request.get(
            "https://example.com/api/v1/data/897?start=100&limit=100", json=[])
        # call the task
        task_fetch_form_instances(xform_id=xform.id)
        # should result in two instances
        self.assertTrue(Instance.objects.filter(ona_pk=21311503).exists())
        self.assertTrue(Instance.objects.filter(ona_pk=21311495).exists())

    @patch('kaznet.apps.ona.tasks.task_fetch_form_instances.delay')
    def test_task_fetch_all_instances(self, mock):
        """
        Test task_fetch_all_instances
        """
        mommy.make('ona.XForm', id=709, deleted_at=timezone.now())
        mommy.make('ona.XForm', id=67, deleted_at=None)
        form1 = mommy.make('ona.XForm', id=99)
        form2 = mommy.make(
            'ona.XForm',
            id=7,
            ona_pk=897,
            id_string='attachment_test',
            title='attachment test')

        mommy.make('main.Task', status=Task.DRAFT, target_content_object=form1)
        mommy.make(
            'main.Task', status=Task.ACTIVE, target_content_object=form2)

        task_fetch_all_instances()
        mock.assert_called_once_with(xform_id=7)

    @patch('kaznet.apps.ona.tasks.task_update_user_profile.delay')
    def test_task_process_user_profiles(self, mock):
        """
        Test update user profiles
        """
        support_user = mommy.make(
            'auth.User', username='onasupport', last_login=timezone.now())
        support_profile = support_user.userprofile

        task_process_user_profiles()
        mock.assert_called_with(ona_username=support_profile.ona_username)
