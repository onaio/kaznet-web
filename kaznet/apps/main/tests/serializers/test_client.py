"""
Test module for ClientSeriliazer
"""
from kaznet.apps.main.serializers import ClientSerializer
from kaznet.apps.main.tests.base import MainTestBase


class TestClientSerializer(MainTestBase):
    """
    Test the ClientSerializer
    """

    def setUp(self):
        super().setUp()

    def test_create_client(self):
        """
        Test that the serializer can create a Client
        """

        data = {
            'name': 'Flux Company'
        }

        serializer_instance = ClientSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        client = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual(client.name, data['name'])

        expected_fields = ['name', 'id', 'created', 'modified']
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
