"""
Module containing Tests for Ona Apps
serializers.py
"""

from django.test import TestCase
from django.utils.text import slugify

from model_mommy import mommy

from kaznet.apps.ona.serializers import (InstanceSerializer, ProjectSerializer,
                                         XFormSerializer)


class TestXFormSerializer(TestCase):
    """
    Tests for XFromSerializer
    """

    def test_serializer_output(self):
        """
        Test that we get fields we are exprecting
        """
        mocked_idstring = slugify('Solar Flare')
        mocked_data = {
            'id': 45,
            'ona_pk': 596,
            'project_id': 54,
            'title': 'Solar Flare',
            'id_string': mocked_idstring
        }

        serializer_data = XFormSerializer(mocked_data).data
        expected_fields = {
            'id',
            'ona_pk',
            'project_id',
            'last_updated',
            'id_string',
            'deleted_at',
            'title',
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))

        self.assertEqual(596, serializer_data['ona_pk'])
        self.assertEqual(54, serializer_data['project_id'])
        self.assertEqual("Solar Flare", serializer_data['title'])
        self.assertEqual(mocked_idstring, serializer_data['id_string'])


class TestInstanceSerializer(TestCase):
    """
    Tests for InstanceSerializer
    """

    def test_serializer_output(self):
        """
        Test that we get the fields we are expecting
        """
        mocked_xform = mommy.make('ona.XForm')
        mocked_data = {
            'id': 34,
            'ona_pk': 596,
            'xform': mocked_xform,
            'json': dict
        }

        serializer_data = InstanceSerializer(mocked_data).data

        expected_fields = {
            'id',
            'ona_pk',
            'xform',
            'last_updated',
            'json',
            'deleted_at'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))
        self.assertEqual(596, serializer_data['ona_pk'])
        self.assertEqual(str(mocked_xform.id), serializer_data['xform']['id'])
        self.assertEqual(dict, serializer_data['json'])


class TestProjectSerializer(TestCase):
    """
    Tests for OnaProjectSerializer
    """

    def test_serializer_output(self):
        """
        Test that we get the fields we are expecting
        """
        mocked_data = {
            'id': 1,
            'ona_pk': 59,
            'organization': 12,
            'name': 'Project Zero'
        }

        serializer_data = ProjectSerializer(mocked_data).data

        expected_fields = {
            'id',
            'ona_pk',
            'organization',
            'last_updated',
            'name',
            'deleted_at'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))

        self.assertEqual(59, serializer_data['ona_pk'])
        self.assertEqual(12, serializer_data['organization'])
        self.assertEqual('Project Zero', serializer_data['name'])
