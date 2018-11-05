"""
Test for Project model
"""

from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase


class TestProject(MainTestBase):
    """
    Test class for TaskProject models
    """

    def setUp(self):
        super().setUp()

    def test_project_model_str(self):
        """
        Test __str__ method of Project model
        """

        livestock_task_list = mommy.make(
            'main.Project',
            name="Livestock tasks")
        expected = "Livestock tasks"
        self.assertEqual(expected, livestock_task_list.__str__())
