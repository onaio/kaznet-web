"""
Module Containing all Tests for
Ona Apps models.py
"""

from model_mommy import mommy

from kaznet.apps.main.models import Task
from kaznet.apps.main.tests.base import MainTestBase


class TestXFormModel(MainTestBase):
    """
    Tests for XFormModel
    """

    def setUp(self):
        super().setUp()

    def test_xform_str(self):
        """
        Test string representation for XForm Model
        """
        xform = mommy.make('ona.XForm', title='Test')
        self.assertEqual(str(xform), 'Test')

    def test_xform_properties(self):
        """
        Test XForm model properties
        """
        xform = mommy.make('ona.XForm', title='Test')
        task = mommy.make(
            'main.Task', name='Coconut', status=Task.ACTIVE,
            target_content_object=xform)
        xform.refresh_from_db()
        self.assertEqual(task, xform.task)
        self.assertEqual('Coconut', xform.task.name)
        self.assertTrue(xform.has_task)
        self.assertEqual(
            list(Task.objects.filter(target_object_id=xform.id)),
            list(xform.tasks))

    def test_delete_xform(self):
        """
        Test that deleting at XForm does not delete the task
        """
        xform = mommy.make('ona.XForm', title='Test')
        task = mommy.make(
            'main.Task', name='Q', status=Task.ACTIVE,
            target_content_object=xform)
        # delete the form
        xform.delete()
        # if the task does not exist, refresh from db will cause an exception
        task.refresh_from_db()
        # check that no form is attached
        self.assertEqual(task.target_object_id, None)
        self.assertEqual(task.target_content_type, None)
        self.assertEqual(task.status, Task.DRAFT)


class TestProjectModel(MainTestBase):
    """
    Tests for ProjectModel
    """

    def setUp(self):
        super().setUp()

    def test_project_str(self):
        """
        Test string representation for Project Model
        """
        project = mommy.make('ona.Project', name='Project Zero')
        self.assertEqual(str(project), 'Project Zero')
