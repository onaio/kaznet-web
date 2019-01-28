"""
Module for testing the Ona app utils
"""
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import override_settings

from dateutil.parser import parse
from django_prices.models import Money
from model_mommy import mommy

from kaznet.apps.main.models import Bounty, Location, Submission, Task
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.apps.ona.utils import (check_if_users_can_submit_to_form,
                                   delete_instance, delete_project,
                                   delete_xform)


class TestUtils(MainTestBase):
    """
    Tests for utils.py
    """

    def setUp(self):
        super().setUp()

    def test_delete_instance(self):
        """
        Test delete_instance
        """
        instance = mommy.make('ona.Instance')
        task = mommy.make('main.Task', name='Quest')
        location = mommy.make('main.Location', name='Voi')
        user = mommy.make('auth.User', first_name='Coco')
        bounty = mommy.make(
            'main.Bounty', task=task, amount=Money('50', 'KES'))
        submission = mommy.make(
            'main.Submission',
            task=task,
            location=location,
            user=user,
            submission_time=parse("2018-09-04T00:00:00+00:00"),
            status=Submission.APPROVED,
            target_object_id=instance.id,
            target_content_type=self.instance_type
        )

        delete_instance(instance=instance)

        # the instance and submission were deleted
        self.assertFalse(Instance.objects.filter(id=instance.id).exists())
        self.assertFalse(Submission.objects.filter(id=submission.id).exists())

        # these other models were not deleted
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_delete_instance_atomic(self):
        """
        Test delete_instance is atomic
        """
        instance = mommy.make('ona.Instance')
        task = mommy.make('main.Task', name='Quest')
        location = mommy.make('main.Location', name='Voi')
        user = mommy.make('auth.User', first_name='Coco')
        bounty = mommy.make(
            'main.Bounty', task=task, amount=Money('50', 'KES'))
        submission = mommy.make(
            'main.Submission',
            task=task,
            location=location,
            user=user,
            submission_time=parse("2018-09-04T00:00:00+00:00"),
            status=Submission.APPROVED,
            target_object_id=instance.id,
            target_content_type=self.instance_type
        )

        with patch('kaznet.apps.main.models.Submission.delete') as mock:
            # we want a database-level error to happen when we attempt to
            # delete a submission
            mock.side_effect = IntegrityError

            # this is necessary so that this test does not fail here
            with self.assertRaises(IntegrityError):
                delete_instance(instance=instance)

        # nothing was deleted
        self.assertTrue(Instance.objects.filter(id=instance.id).exists())
        self.assertTrue(Submission.objects.filter(id=submission.id).exists())
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        with patch('kaznet.apps.ona.models.Instance.delete') as mock:
            # we want a database-level error to happen when we attempt to
            # delete an instance
            mock.side_effect = IntegrityError

            # this is necessary so that this test does not fail here
            with self.assertRaises(IntegrityError):
                delete_instance(instance=instance)

        # STILL nothing was deleted
        self.assertTrue(Instance.objects.filter(id=instance.id).exists())
        self.assertTrue(Submission.objects.filter(id=submission.id).exists())
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_delete_xform(self):
        """
        Test delete_xform
        """
        xform = mommy.make('ona.XForm')
        instance = mommy.make('ona.Instance', xform=xform)
        task = mommy.make(
            'main.Task', name='Quest',
            target_object_id=xform.id,
            target_content_type=self.xform_type,
            status=Task.ACTIVE
        )
        location = mommy.make('main.Location', name='Voi')
        user = mommy.make('auth.User', first_name='Coco')
        bounty = mommy.make(
            'main.Bounty', task=task, amount=Money('50', 'KES'))
        submission = mommy.make(
            'main.Submission',
            task=task,
            location=location,
            user=user,
            submission_time=parse("2018-09-04T00:00:00+00:00"),
            status=Submission.APPROVED,
            target_object_id=instance.id,
            target_content_type=self.instance_type
        )

        delete_xform(xform=xform)

        # the xform, instance and submission were deleted
        self.assertFalse(XForm.objects.filter(id=xform.id).exists())
        self.assertFalse(Instance.objects.filter(id=instance.id).exists())
        self.assertFalse(Submission.objects.filter(id=submission.id).exists())

        # these other models were not deleted
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        # the task is now draft
        task.refresh_from_db()
        self.assertEqual(Task.DRAFT, task.status)

    def test_delete_xform_atomic(self):
        """
        Test delete_xform is atomic
        """
        xform = mommy.make('ona.XForm')
        instance = mommy.make('ona.Instance', xform=xform)
        task = mommy.make(
            'main.Task', name='Quest',
            target_object_id=xform.id,
            target_content_type=self.xform_type,
            status=Task.ACTIVE
        )
        location = mommy.make('main.Location', name='Voi')
        user = mommy.make('auth.User', first_name='Coco')
        bounty = mommy.make(
            'main.Bounty', task=task, amount=Money('50', 'KES'))
        submission = mommy.make(
            'main.Submission',
            task=task,
            location=location,
            user=user,
            submission_time=parse("2018-09-04T00:00:00+00:00"),
            status=Submission.APPROVED,
            target_object_id=instance.id,
            target_content_type=self.instance_type
        )

        with patch('kaznet.apps.ona.utils.delete_instance') as mock:
            # we want a database-level error to happen when we attempt to
            # delete an instance or a submission
            mock.side_effect = IntegrityError

            # this is necessary so that this test does not fail here
            with self.assertRaises(IntegrityError):
                delete_xform(xform=xform)

        # nothing was deleted
        self.assertTrue(XForm.objects.filter(id=xform.id).exists())
        self.assertTrue(Instance.objects.filter(id=instance.id).exists())
        self.assertTrue(Submission.objects.filter(id=submission.id).exists())
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        # the task status did not change
        task.refresh_from_db()
        self.assertEqual(Task.ACTIVE, task.status)

        with patch('kaznet.apps.ona.models.XForm.delete') as mock:
            # we want a database-level error to happen when we attempt to
            # delete an xform
            mock.side_effect = IntegrityError

            # this is necessary so that this test does not fail here
            with self.assertRaises(IntegrityError):
                delete_xform(xform=xform)

        # nothing was deleted
        self.assertTrue(XForm.objects.filter(id=xform.id).exists())
        self.assertTrue(Instance.objects.filter(id=instance.id).exists())
        self.assertTrue(Submission.objects.filter(id=submission.id).exists())
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        # the task status did not change
        task.refresh_from_db()
        self.assertEqual(Task.ACTIVE, task.status)

    def test_delete_project(self):
        """
        Test delete_xform
        """
        project = mommy.make('ona.Project')
        xform = mommy.make('ona.XForm', project=project)
        xform2 = mommy.make('ona.XForm', ona_project_id=project.ona_pk)
        instance = mommy.make('ona.Instance', xform=xform)
        task = mommy.make(
            'main.Task', name='Quest',
            target_object_id=xform.id,
            target_content_type=self.xform_type,
            status=Task.ACTIVE
        )
        location = mommy.make('main.Location', name='Voi')
        user = mommy.make('auth.User', first_name='Coco')
        bounty = mommy.make(
            'main.Bounty', task=task, amount=Money('50', 'KES'))
        submission = mommy.make(
            'main.Submission',
            task=task,
            location=location,
            user=user,
            submission_time=parse("2018-09-04T00:00:00+00:00"),
            status=Submission.APPROVED,
            target_object_id=instance.id,
            target_content_type=self.instance_type
        )

        delete_project(project=project)

        # the Project, XForm, Instance and Submission were deleted
        self.assertFalse(Project.objects.filter(id=project.id).exists())
        self.assertFalse(XForm.objects.filter(id=xform.id).exists())
        self.assertFalse(XForm.objects.filter(id=xform2.id).exists())
        self.assertFalse(Instance.objects.filter(id=instance.id).exists())
        self.assertFalse(Submission.objects.filter(id=submission.id).exists())

        # these other models were not deleted
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        # the task is now draft
        task.refresh_from_db()
        self.assertEqual(Task.DRAFT, task.status)

    def test_delete_project_atomic(self):
        """
        Test delete_project is atomic
        """
        project = mommy.make('ona.Project')
        xform = mommy.make('ona.XForm', project=project)
        xform2 = mommy.make('ona.XForm', ona_project_id=project.ona_pk)
        instance = mommy.make('ona.Instance', xform=xform)
        task = mommy.make(
            'main.Task', name='Quest',
            target_object_id=xform.id,
            target_content_type=self.xform_type,
            status=Task.ACTIVE
        )
        location = mommy.make('main.Location', name='Voi')
        user = mommy.make('auth.User', first_name='Coco')
        bounty = mommy.make(
            'main.Bounty', task=task, amount=Money('50', 'KES'))
        submission = mommy.make(
            'main.Submission',
            task=task,
            location=location,
            user=user,
            submission_time=parse("2018-09-04T00:00:00+00:00"),
            status=Submission.APPROVED,
            target_object_id=instance.id,
            target_content_type=self.instance_type
        )

        with patch('kaznet.apps.ona.models.Project.delete') as mock:
            # we want a database-level error to happen when we attempt to
            # delete a project
            mock.side_effect = IntegrityError

            # this is necessary so that this test does not fail here
            with self.assertRaises(IntegrityError):
                delete_project(project=project)

        # nothing deleted
        self.assertTrue(Project.objects.filter(id=project.id).exists())
        self.assertTrue(XForm.objects.filter(id=xform.id).exists())
        self.assertTrue(XForm.objects.filter(id=xform2.id).exists())
        self.assertTrue(Instance.objects.filter(id=instance.id).exists())
        self.assertTrue(Submission.objects.filter(id=submission.id).exists())
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        # the task status did not change
        task.refresh_from_db()
        self.assertEqual(Task.ACTIVE, task.status)

        with patch('kaznet.apps.ona.utils.delete_xform') as mock:
            # we want a database-level error to happen when we attempt to
            # delete an xform, instance or submission
            mock.side_effect = IntegrityError

            # this is necessary so that this test does not fail here
            with self.assertRaises(IntegrityError):
                delete_project(project=project)

        # nothing deleted
        self.assertTrue(Project.objects.filter(id=project.id).exists())
        self.assertTrue(XForm.objects.filter(id=xform.id).exists())
        self.assertTrue(XForm.objects.filter(id=xform2.id).exists())
        self.assertTrue(Instance.objects.filter(id=instance.id).exists())
        self.assertTrue(Submission.objects.filter(id=submission.id).exists())
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        # the task status did not change
        task.refresh_from_db()
        self.assertEqual(Task.ACTIVE, task.status)

        with patch('kaznet.apps.ona.utils.delete_instance') as mock:
            # we want a database-level error to happen when we attempt to
            # delete an instance or a submission
            mock.side_effect = IntegrityError

            # this is necessary so that this test does not fail here
            with self.assertRaises(IntegrityError):
                delete_project(project=project)

        # nothing deleted
        self.assertTrue(Project.objects.filter(id=project.id).exists())
        self.assertTrue(XForm.objects.filter(id=xform.id).exists())
        self.assertTrue(XForm.objects.filter(id=xform2.id).exists())
        self.assertTrue(Instance.objects.filter(id=instance.id).exists())
        self.assertTrue(Submission.objects.filter(id=submission.id).exists())
        self.assertTrue(Bounty.objects.filter(id=bounty.id).exists())
        self.assertTrue(Location.objects.filter(id=location.id).exists())
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        # the task status did not change
        task.refresh_from_db()
        self.assertEqual(Task.ACTIVE, task.status)

    @override_settings(
        ONA_ORG_NAME='onasystemsinc',
        ONA_XFORM_CONFIGURED_FIELD='configuration_status',
        ONA_CONTRIBUTER_ROLE="dataentry"
    )
    def test_check_if_users_can_submit_to_form(self):
        """Test check_if_users_can_submit_to_form"""
        # test correct
        project = mommy.make(
            'ona.Project',
            name="Test Project",
            json={
                "url": "https://api.ona.io/api/v1/projects/1337",
                "name": "Test Project",
                "forms": [{
                    "name": "Test Form",
                }],
                "owner": "https://api.ona.io/api/v1/users/onasystemsinc",
                "teams": [{
                    "name": "onasystemsinc#members",
                    "role": "dataentry",
                    "users": ["mosh"]
                }, {
                    "name": "onasystemsinc#Owners",
                    "role": "owner",
                    "users": ["coco"]
                }],
            }
        )
        xform = mommy.make(
            'ona.XForm',
            title="Test Form",
            ona_project_id=project.ona_pk,
            json={"owner": "onasystemsinc"}
        )
        check_if_users_can_submit_to_form(xform)
        xform.refresh_from_db()
        self.assertEqual(
            XForm.CORRECTLY_CONFIGURED,
            xform.json[settings.ONA_XFORM_CONFIGURED_FIELD]
        )
