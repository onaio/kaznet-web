# -*- coding: utf-8 -*-
"""
Test for Location model
"""
from django.test import TestCase

from model_mommy import mommy


class TestLocations(TestCase):
    """
    Test class for Location models
    """

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
