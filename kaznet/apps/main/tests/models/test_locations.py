# -*- coding: utf-8 -*-
"""
Test for Location model
"""
from __future__ import unicode_literals

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
