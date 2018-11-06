"""
Test for Location model
"""
from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase


class TestLocations(MainTestBase):
    """
    Test class for Location models
    """

    def setUp(self):
        super().setUp()

    def test_location_model_str(self):
        """
        Test the str method on Location model with Country Defined
        """
        nairobi = mommy.make(
            'main.Location',
            name="Nairobi",
            country="KE")
        expected = 'Kenya - Nairobi'
        self.assertEqual(expected, nairobi.__str__())

    def test_location_model_str_no_country(self):
        """
        Test the str method on Location model without Country Defined
        """
        nairobi = mommy.make('main.Location', name="Nairobi")
        expected = 'Nairobi'
        self.assertEqual(expected, nairobi.__str__())

    def test_location_parent_link(self):
        """
        Test the parent link between Locations
        """
        nairobi = mommy.make('main.Location', name="Nairobi")
        hurlingham = mommy.make(
            'main.Location',
            name="Hurlingham",
            parent=nairobi)
        self.assertEqual(nairobi, hurlingham.parent)

    def test_parent_name(self):
        """
        Test parent name
        """
        nairobi = mommy.make('main.Location', name="Nairobi")
        hurlingham = mommy.make(
            'main.Location',
            name="Hurlingham",
            parent=nairobi)
        self.assertEqual(None, nairobi.parent_name)
        self.assertEqual("Nairobi", hurlingham.parent_name)

    def test_has_submissions(self):
        """
        Test the has_submissions property
        """
        nairobi = mommy.make('main.Location', name="Nairobi")
        voi = mommy.make('main.Location', name="Voi")
        # make a Voi submission
        mommy.make(
            'main.Submission',
            location=voi,
            _fill_optional=['user', 'comment', 'submission_time'])
        self.assertEqual(False, nairobi.has_submissions)
        self.assertEqual(True, voi.has_submissions)

    def test_location_type_name(self):
        """
        Test location_type_name
        """
        market = mommy.make('main.LocationType', name="Market")
        nairobi = mommy.make('main.Location', name="Nairobi")
        hurlingham = mommy.make(
            'main.Location',
            name="Hurlingham",
            location_type=market)
        self.assertEqual(None, nairobi.location_type_name)
        self.assertEqual("Market", hurlingham.location_type_name)
