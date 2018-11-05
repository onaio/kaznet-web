"""
Tests for KaznetContentTypeSerializer
"""
from django.contrib.contenttypes.models import ContentType

from kaznet.apps.main.serializers import KaznetContentTypeSerializer
from kaznet.apps.main.tests.base import MainTestBase


class TestKaznetContentTypeSerializer(MainTestBase):
    """
    Tests the KaznetContentTypeSerializer
    """

    def setUp(self):
        super().setUp()

    def test_serializer_output(self):
        """
        Test that the serializer returns the expected fields
        """
        mocked_contenttype = ContentType.objects.filter(
            app_label='ona', model='xform').first()

        serializer_data = KaznetContentTypeSerializer(mocked_contenttype).data

        expected_fields = {
            'app_label',
            'model',
            'id'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))
        self.assertEqual(
            mocked_contenttype.app_label, serializer_data['app_label'])
        self.assertEqual(
            mocked_contenttype.model, serializer_data['model'])
        self.assertEqual(
            mocked_contenttype.id, serializer_data['id'])
