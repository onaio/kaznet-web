"""
Test module for celery tasks for Ona app
"""
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings

import requests_mock

from kaznet.apps.ona.models import Project, XForm
from kaznet.apps.ona.tasks import (task_fetch_project_xforms,
                                   task_fetch_projects)

MOCK_PROJECT_DATA = [
    {
        "projectid": 1337,
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
        "name": "Project of Life",
        "date_modified": "2018-05-30T07:51:59.267839Z",
        "deleted_at": None
    },
    {
        "projectid": 1333337,
        "forms": [],
        "name": "Hunter2",
        "date_modified": "2018-05-30T07:51:59.267839Z",
        "deleted_at": None
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
    def test_task_fetch_projects(
            self, mocked_process_projects, mocked_fetch_project_task,
            mocked_request):
        """
        Test task_fetch_projects
        """
        # mock the request
        mocked_request.get(
            "https://example.com/api/v1/projects?owner=mosh",
            json=MOCK_PROJECT_DATA
        )
        # run the task
        task_fetch_projects(username=settings.ONA_USERNAME)
        # we should call process_projects
        mocked_process_projects.assert_called_with(MOCK_PROJECT_DATA)
        # we should call task_fetch_project_xforms twice, for each form
        self.assertEqual(1, mocked_fetch_project_task.call_count)
        mocked_fetch_project_task.assert_called_with(
            forms=MOCK_PROJECT_DATA[0]['forms'],
            project_id=MOCK_PROJECT_DATA[0]['projectid']
        )

    @patch('kaznet.apps.ona.tasks.process_xforms')
    def test_task_fetch_project_xforms(self, mock):
        """
        Test task_fetch_project_xforms
        """
        # call the task
        task_fetch_project_xforms(
            MOCK_PROJECT_DATA[0]['forms'][1],
            MOCK_PROJECT_DATA[0]['projectid'])
        # we should have called process_xforms
        mock.assert_called_with(
            forms_data=MOCK_PROJECT_DATA[0]['forms'][1],
            project_id=MOCK_PROJECT_DATA[0]['projectid']
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
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
            json=MOCK_PROJECT_DATA
        )
        # run the task
        task_fetch_projects(username=settings.ONA_USERNAME)
        # we should have two projects
        self.assertTrue(Project.objects.filter(ona_pk=1337).exists())
        self.assertTrue(Project.objects.filter(ona_pk=1333337).exists())
        # we should have two forms
        self.assertTrue(XForm.objects.filter(ona_pk=7331).exists())
        self.assertTrue(XForm.objects.filter(ona_pk=310).exists())
