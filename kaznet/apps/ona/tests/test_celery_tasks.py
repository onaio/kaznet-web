"""
Test module for celery tasks for Ona app
"""
from unittest.mock import call, patch
from urllib.parse import urljoin

import requests_mock
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import override_settings
from django.utils import timezone
from model_mommy import mommy

from kaznet.apps.main.models import Task
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.apps.ona.tasks import (task_auto_create_filtered_data_sets,
                                   task_check_if_users_can_submit_to_form,
                                   task_create_form_webhook,
                                   task_fetch_form_missing_instances,
                                   task_fetch_missing_instances,
                                   task_fetch_projects,
                                   task_process_project_xforms,
                                   task_process_user_profiles,
                                   task_sync_deleted_instances,
                                   task_sync_deleted_projects,
                                   task_sync_deleted_xforms,
                                   task_sync_form_deleted_instances,
                                   task_sync_form_updated_instances,
                                   task_sync_updated_instances,
                                   task_sync_xform_can_submit_checks,
                                   task_update_user_profile,
                                   task_sync_outdated_submission_reviews)
from kaznet.apps.ona.tests.test_api import MOCKED_ONA_FORM_DATA

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
        "_media_all_received": True,
        "_bamboo_dataset_id": "",
        "_tags": [],
        "_xform_id_string": "attachment_test",
        "meta/instanceID": "uuid:65903eb7-6524-4f81-89df-5a3cc725910e",
        "_duration": "",
        "_geolocation": [None, None],
        "_edited": False,
        "_status": "submitted_via_web",
        "_uuid": "65903eb7-6524-4f81-89df-5a3cc725910e",
        "_submitted_by": "onasupport",
        "image1": "reece-12_48_29.JPG",
        "_media_count": 1,
        "formhub/uuid": "fff2652efcd24709bb9236d24c77e918",
        "name": "ALLLIIICCCEE",
        "_total_media": 1,
        "_xform_id": 253470,
        "_submission_time": "2017-10-30T09:50:47",
        "_version": "201710300941",
        "_attachments": [],
        "_id": 21311503,
        "_review_status": settings.ONA_SUBMISSION_REVIEW_REJECTED,
        "_review_comment": "",
    },
]


class TestCeleryTasks(MainTestBase):
    """
    Tests for celery tasks
    """

    def setUp(self):
        super().setUp()

    @override_settings(ONA_BASE_URL="https://example.com", ONA_USERNAME='mosh')
    @patch('kaznet.apps.ona.tasks.task_process_project_xforms.delay')
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
        # we should call task_process_project_xforms twice, for each form
        self.assertEqual(1, mocked_fetch_project_task.call_count)
        mocked_fetch_project_task.assert_called_with(
            forms=MOCK_PROJECT_DATA[0]['forms'],
            project_id=MOCK_PROJECT_DATA[0]['projectid'])

    @patch('kaznet.apps.ona.tasks.get_and_process_xforms')
    def test_task_process_project_xforms(self, mock):
        """
        Test task_process_project_xforms
        """
        # call the task
        task_process_project_xforms(
            MOCK_PROJECT_DATA[0]['forms'][1],
            MOCK_PROJECT_DATA[0]['projectid'])
        # we should have called get_and_process_xforms
        mock.assert_called_with(
            forms_data=MOCK_PROJECT_DATA[0]['forms'][1],
            project_id=MOCK_PROJECT_DATA[0]['projectid'])

    @override_settings(
        CELERY_TASK_ALWAYS_EAGER=True,
        ONA_BASE_URL="https://example.com",
        ONA_USERNAME='mosh')
    @requests_mock.Mocker()
    @patch('kaznet.apps.ona.api.get_xform')
    def test_fetch_projects_and_xforms(self, mocked_request, get_xform_mock):
        """
        Test that the `task_fetch_projects` task actually fetches and
        stores projects and XForms
        """

        def _get_xform(*args, **kwargs):
            arguments = args
            if arguments[0] == 7331:
                return {
                    "name": "Form 66",
                    "formid": 7331,
                    "id_string": "aFEjJKzULJbQYsmQzKcpL9",
                    "is_merged_dataset": False,
                    "version": "v5555555555",
                    "owner": "https://example.com/api/v1/users/kaznet"
                }
            elif arguments[0] == 310:
                return {
                    "name": "Q-q-uest",
                    "formid": 310,
                    "id_string": "kjoin_zKcpL9",
                    "is_merged_dataset": False,
                    "version": "v1111111111",
                    "owner": "https://example.com/api/v1/users/kaznet"
                }

            return None

        get_xform_mock.side_effect = _get_xform

        # mock the request
        mocked_request.get(
            "https://example.com/api/v1/projects?owner=mosh",
            json=MOCK_PROJECT_DATA)
        mocked_request.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/7331/form.json'),
            json=MOCKED_ONA_FORM_DATA
        )
        mocked_request.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/forms/310/form.json'),
            json=MOCKED_ONA_FORM_DATA
        )
        mocked_request.post(
            urljoin(settings.ONA_BASE_URL, 'api/v1/dataviews'),
            status_code=201
        )
        # run the task
        task_fetch_projects(username=settings.ONA_USERNAME)
        # we should have two projects
        self.assertTrue(Project.objects.filter(ona_pk=1337).exists())
        self.assertTrue(Project.objects.filter(ona_pk=1333337).exists())
        # we should have two forms
        self.assertTrue(XForm.objects.filter(ona_pk=7331).exists())
        self.assertTrue(XForm.objects.filter(ona_pk=310).exists())

    @patch('kaznet.apps.ona.tasks.fetch_missing_instances')
    def test_task_fetch_form_missing_instances(
            self, fetch_missing_instances_mock):
        """
        Test task_fetch_form_missing_instances
        """
        mommy.make('auth.User', username='onasupport')
        xform = mommy.make(
            'ona.XForm',
            id=7,
            ona_pk=897,
            id_string='attachment_test',
            title='attachment test')
        # call the task
        task_fetch_form_missing_instances(xform_id=xform.id)
        # fetch_missing_instances_mock should have been called once
        self.assertEqual(1, fetch_missing_instances_mock.call_count)

        expected_calls = [
            call(form_id=xform.ona_pk)
        ]

        fetch_missing_instances_mock.assert_has_calls(expected_calls)

    @override_settings(ONA_BASE_URL="https://example.com")
    @requests_mock.Mocker()
    def test_task_fetch_form_missing_instances_integration(
            self, mocked_request):
        """
        Test task_fetch_form_missing_instances results in actual instances
        """
        mommy.make('auth.User', username='onasupport')
        Instance.objects.all().delete()

        # mock the request to get submission ids
        mocked_ids = [
            {"_id": 21311495},
            {"_id": 21311503},
        ]
        mocked_request.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/data/897.json'),
            json=mocked_ids
        )

        # mock the request to create a webook
        mocked_request.post(
            urljoin(settings.ONA_BASE_URL, 'api/v1/dataviews'),
            status_code=201
        )

        # create XForm
        xform = mommy.make(
            'ona.XForm',
            id=7,
            ona_pk=897,
            id_string='attachment_test',
            title='attachment test')

        # mock the requests for individual submissions
        mocked_request.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/data/897/21311495.json'),
            json=MOCKED_INSTANCES[0])
        mocked_request.get(
            urljoin(settings.ONA_BASE_URL, '/api/v1/data/897/21311503.json'),
            json=MOCKED_INSTANCES[1])

        # call the task
        task_fetch_form_missing_instances(xform_id=xform.id)

        # should result in two instances
        self.assertTrue(Instance.objects.filter(ona_pk=21311503).exists())
        self.assertTrue(Instance.objects.filter(ona_pk=21311495).exists())

    @patch('kaznet.apps.ona.tasks.task_fetch_form_missing_instances.delay')
    def test_task_fetch_missing_instances(self, mock):
        """
        Test task_fetch_missing_instances
        """
        XForm.objects.all().delete()
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

        task_fetch_missing_instances()
        mock.assert_called_once_with(xform_id=7)

    @override_settings(
        CELERY_TASK_ALWAYS_EAGER=True,
        ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    @patch('kaznet.apps.ona.api.process_instance')
    def test_task_fetch_missing_instances_404_at_form(
            self, mocked_request, process_instance_mock):
        """
        Test what happens when task_fetch_missing_instances encounters
        404 errors
        """
        XForm.objects.all().delete()

        # create two forms
        form1 = mommy.make('ona.XForm', id=709, deleted_at=timezone.now())
        form2 = mommy.make('ona.XForm', id=67, deleted_at=None)

        # create tasks for the two forms
        mommy.make('main.Task', status=Task.DRAFT, target_content_object=form1)
        mommy.make(
            'main.Task', status=Task.ACTIVE, target_content_object=form2)

        # should get 404 at form level
        raw_ids_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{form2.ona_pk}.json')
        mocked_request.get(raw_ids_url, text='Not Found', status_code=404)

        # only form 2 should run
        task_fetch_missing_instances()

        # should only have called the requests mock once
        self.assertEqual(1, mocked_request.call_count)

        # you'll never get to process_instance
        self.assertFalse(process_instance_mock.called)

    @override_settings(
        CELERY_TASK_ALWAYS_EAGER=True,
        ONA_BASE_URL='https://mosh-ona.io')
    @requests_mock.Mocker()
    @patch('kaznet.apps.ona.api.process_instance')
    def test_task_fetch_missing_instances_404_at_instance(
            self, mocked_request, process_instance_mock):
        """
        Test what happens when task_fetch_missing_instances encounters
        404 errors
        """
        XForm.objects.all().delete()
        Instance.objects.all().delete()

        # create two forms
        form1 = mommy.make('ona.XForm', id=709, deleted_at=timezone.now())
        form2 = mommy.make('ona.XForm', id=67, deleted_at=None)

        # create tasks for the two forms
        mommy.make('main.Task', status=Task.DRAFT, target_content_object=form1)
        mommy.make(
            'main.Task', status=Task.ACTIVE, target_content_object=form2)

        # should not get 404 at form level
        mocked_ids_response = [
            {"_id": 1755}, {"_id": 1757}
        ]
        raw_ids_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{form2.ona_pk}.json')
        mocked_request.get(
            raw_ids_url, json=mocked_ids_response, status_code=200)

        # should get 404 at one instance
        sub2_response = {
            "_xform_id_string": "aFEjJKzULJbQYsmQzKcpL9",
            "_edited": False,
            "_last_edited": "2018-05-30T07:51:59.187363+00:00",
            "_xform_id": form2.ona_pk,
            "_id": 1757
        }

        submission1_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{form2.ona_pk}/1755.json')
        mocked_request.get(
            submission1_url,
            text='Not found',
            status_code=404)

        submission2_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/data/{form2.ona_pk}/1757.json')
        mocked_request.get(
            submission2_url,
            json=sub2_response,
            status_code=200)

        # only form 2 should run as it is not deleted
        task_fetch_missing_instances()

        # should have called the requests mock once
        self.assertEqual(3, mocked_request.call_count)

        # you'll get to process_instance only once
        self.assertEqual(1, process_instance_mock.call_count)
        process_instance_mock.assert_called_once_with(
            instance_data=sub2_response, xform=form2
        )

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

    @patch('kaznet.apps.ona.tasks.update_user_profile_metadata')
    def test_task_update_user_profile(self, mock):
        """
        Test that task_update_user_profile actually calls
        update_user_profile_metadata
        """
        task_update_user_profile('Dave')

        mock.assert_called_once_with('Dave')

    @patch('kaznet.apps.ona.tasks.create_filtered_data_sets')
    def test_task_auto_create_filtered_data_sets(self, mock):
        """
        Test task_auto_create_filtered_data_sets
        """
        ona_form = mommy.make(
            'ona.XForm',
            ona_pk=100,
            ona_project_id=1542,
            title='Test Form'
        )
        task_auto_create_filtered_data_sets(
            form_id=ona_form.ona_pk,
            project_id=ona_form.ona_project_id,
            form_title=ona_form.title)
        mock.assert_called_with(
            form_id=ona_form.ona_pk,
            project_id=ona_form.ona_project_id,
            form_title=ona_form.title)

    @patch('kaznet.apps.ona.tasks.create_form_webhook')
    def test_task_create_form_webhook(self, mock):
        """
        Test task_create_form_webhook
        """
        current_site = Site.objects.get_current()
        current_site.domain = "https://kaznet.com"
        current_site.save()

        task_create_form_webhook(form_id=1337)
        mock.assert_called_with(
            form_id=1337,
            service_url="https://kaznet.com/webhook/")

    @patch('kaznet.apps.ona.tasks.task_sync_form_updated_instances.delay')
    def test_task_sync_updated_instances(self, mock):
        """
        Test task_sync_updated_instances
        """
        XForm.objects.all().delete()
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

        task_sync_updated_instances()
        mock.assert_called_once_with(xform_id=7)

    @patch('kaznet.apps.ona.tasks.sync_updated_instances')
    def test_task_sync_form_updated_instances(
            self, sync_updated_instances_mock):
        """
        Test task_sync_form_updated_instances
        """
        mommy.make('auth.User', username='onasupport')
        xform = mommy.make(
            'ona.XForm',
            id=7,
            ona_pk=897,
            id_string='attachment_test',
            title='attachment test')
        # call the task
        task_sync_form_updated_instances(xform_id=xform.id)
        # fetch_missing_instances_mock should have been called once
        self.assertEqual(1, sync_updated_instances_mock.call_count)

        expected_calls = [
            call(form_id=xform.ona_pk)
        ]

        sync_updated_instances_mock.assert_has_calls(expected_calls)

    @patch('kaznet.apps.ona.tasks.task_sync_form_deleted_instances.delay')
    def test_task_sync_deleted_instances(self, mock):
        """
        Test task_sync_deleted_instances
        """
        XForm.objects.all().delete()
        form1 = mommy.make('ona.XForm', id=67, deleted_at=None)
        form2 = mommy.make(
            'ona.XForm',
            id=7,
            ona_pk=897,
            id_string='attachment_test',
            title='attachment test')

        task_sync_deleted_instances()

        expected_calls = [
            call(xform_id=form2.id),
            call(xform_id=form1.id),
        ]

        mock.assert_has_calls(expected_calls)

    @patch('kaznet.apps.ona.tasks.sync_deleted_instances')
    def test_task_sync_form_deleted_instances(
            self, sync_deleted_instances_mock):
        """
        Test task_sync_form_deleted_instances
        """
        mommy.make('auth.User', username='onasupport')
        xform = mommy.make(
            'ona.XForm',
            id=7,
            ona_pk=897,
            id_string='attachment_test',
            title='attachment test')
        # call the task
        task_sync_form_deleted_instances(xform_id=xform.id)
        # fetch_missing_instances_mock should have been called once
        self.assertEqual(1, sync_deleted_instances_mock.call_count)

        expected_calls = [
            call(form_id=xform.ona_pk)
        ]

        sync_deleted_instances_mock.assert_has_calls(expected_calls)

    @patch('kaznet.apps.ona.tasks.sync_deleted_xforms')
    def test_task_sync_deleted_xforms(self, mock):
        """
        Test task_sync_deleted_xforms
        """
        # call the task
        task_sync_deleted_xforms(username="mosh")
        mock.assert_called_once_with(username="mosh")

    @patch('kaznet.apps.ona.tasks.sync_deleted_projects')
    def test_task_sync_deleted_projects(self, mock):
        """
        Test task_sync_deleted_projects
        """
        # call the task
        task_sync_deleted_projects(usernames=["coco", "mosh"])
        mock.assert_called_once_with(usernames=["coco", "mosh"])

    @patch(
        'kaznet.apps.ona.tasks.task_check_if_users_can_submit_to_form.delay')
    def test_task_sync_xform_can_submit_checks(self, mock):
        """
        Test task_sync_xform_can_submit_checks
        """
        XForm.objects.all().delete()
        form1 = mommy.make('ona.XForm', deleted_at=None)
        form2 = mommy.make('ona.XForm', deleted_at=None)

        task_sync_xform_can_submit_checks()

        expected_calls = [
            call(xform_id=form2.id),
            call(xform_id=form1.id),
        ]

        mock.assert_has_calls(expected_calls, any_order=True)

    @patch('kaznet.apps.ona.tasks.check_if_users_can_submit_to_form')
    def test_task_check_if_users_can_submit_to_form(self, mock):
        """
        Test task_check_if_users_can_submit_to_form
        """
        XForm.objects.all().delete()
        form1 = mommy.make('ona.XForm', deleted_at=None)

        task_check_if_users_can_submit_to_form(xform_id=form1.id)

        mock.assert_called_once_with(xform=form1)

    @patch('kaznet.apps.ona.tasks.task_sync_submission_review')
    def test_task_sync_outdated_submission_reviews(self, mock):
        """
        Test task_sync_outdated_submission_reviews
        """
        # create 13 instance objects
        initial_ona_pk = 55555
        for i in range(13):
            initial_ona_pk += 1
            instance = mommy.make('ona.Instance', ona_pk=initial_ona_pk)

        instances = Instance.objects.all()
        # set status and comment values for all
        for instance in instances:
            instance.json["status"] = 1
            instance.json["comment"] = ""
            instance.save()

        # mark first 5 as synced with ona data;
        # so the other 8 aren't synced;
        # and neet to be synced
        for i in range(5):
            instances[i].json["synced_with_ona_data"] = True
            instances[i].save()

        # call task_sync_outdated_submission_reviews
        task_sync_outdated_submission_reviews()

        self.assertEqual(mock.delay.call_count, 8)
