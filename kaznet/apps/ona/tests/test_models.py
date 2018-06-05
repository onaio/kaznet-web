"""
Module Containing all Tests for
kaznet.apps.ona.models
"""

from django.test import TestCase
from model_mommy import mommy


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
