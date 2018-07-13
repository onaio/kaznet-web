"""
Test for LocationType Serializers
"""
from django.test import TestCase

from kaznet.apps.main.serializers import KaznetLocationTypeSerializer


class TestKaznetLocationTypeSerializer(TestCase):
    """
    Test the LocationType Serializer
    """

    def test_create_locationtype(self):
        """
        Test that the serializer can create LocationType objects
        """

        data = {
            'name': "Household",
        }

        serializer_instance = KaznetLocationTypeSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        locationtype = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual('Household', locationtype.name)

        expected_fields = [
            'id',
            'created',
            'name',
            'modified'
        ]

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
