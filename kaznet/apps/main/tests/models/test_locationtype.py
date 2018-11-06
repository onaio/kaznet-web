"""
Test for LocationType model
"""
from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase


class TestLocationTypes(MainTestBase):
    """
    Test class for LocationType model
    """

    def setUp(self):
        super().setUp()

    def test_locationtype_model_str(self):
        """
        Test the str method on LocationType model
        """
        waterfront = mommy.make(
            'main.LocationType',
            name="Waterfront")
        expected = 'Waterfront'
        self.assertEqual(expected, waterfront.__str__())
