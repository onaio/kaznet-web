"""
Module containing Tests for Ona Apps
serializers.py
"""
from django.test import TestCase
from django.utils.text import slugify

from model_mommy import mommy
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.ona.serializers import (InstanceSerializer, ProjectSerializer,
                                         XFormSerializer)


class TestXFormSerializer(MainTestBase):
    """
    Tests for XFromSerializer
    """

    def setUp(self):
        super().setUp()

    def test_serializer_output(self):
        """
        Test that we get fields we are exprecting
        """
        mocked_idstring = slugify('Solar Flare')
        mocked_project = mommy.make(
            'ona.Project',
            id=10,
            ona_pk=59,
            organization=12,
            name='Project Zero'
        )
        xform = mommy.make(
            'ona.XForm',
            id=45,
            ona_pk=596,
            project_id=54,
            title='Solar Flare',
            id_string=mocked_idstring,
            kaznet_project=mocked_project
        )

        serializer_instance = XFormSerializer(xform)
        serializer_data = serializer_instance.data
        expected_fields = {
            'id',
            'ona_pk',
            'project_id',
            'last_updated',
            'id_string',
            'deleted_at',
            'title',
            'has_task',
            'created',
            'modified',
            'kaznet_project'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))

        self.assertEqual(596, serializer_data['ona_pk'])
        self.assertEqual(False, serializer_data['has_task'])
        self.assertEqual(54, serializer_data['project_id'])
        self.assertEqual("Solar Flare", serializer_data['title'])
        self.assertEqual(mocked_idstring, serializer_data['id_string'])
        self.assertEqual('10', serializer_data['kaznet_project']['id'])

    def test_has_task(self):
        """
        Test XFormSerializer has_task
        """
        xform = mommy.make(
            'ona.XForm',
            id=45,
            ona_pk=596,
            project_id=54,
            title='Coconut',
            id_string='coconut'
        )
        serializer_instance1 = XFormSerializer(xform)
        self.assertEqual(False, serializer_instance1.data['has_task'])
        mommy.make('main.Task', target_content_object=xform)
        serializer_instance2 = XFormSerializer(xform)
        self.assertEqual(True, serializer_instance2.data['has_task'])


class TestInstanceSerializer(TestCase):
    """
    Tests for InstanceSerializer
    """

    def test_serializer_output(self):
        """
        Test that we get the fields we are expecting
        """
        mocked_xform = mommy.make('ona.XForm')
        mocked_instance = mommy.make(
            'ona.Instance',
            id=34,
            ona_pk=596,
            xform=mocked_xform,
            json={}
            )

        serializer_data = InstanceSerializer(mocked_instance).data

        expected_fields = {
            'id',
            'ona_pk',
            'xform',
            'modified',
            'created',
            'last_updated',
            'json',
            'deleted_at'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))
        self.assertEqual(596, serializer_data['ona_pk'])
        self.assertEqual(str(mocked_xform.id), serializer_data['xform']['id'])
        self.assertEqual({}, serializer_data['json'])


class TestProjectSerializer(TestCase):
    """
    Tests for OnaProjectSerializer
    """

    def test_serializer_output(self):
        """
        Test that we get the fields we are expecting
        """
        mocked_project = mommy.make(
            'ona.Project',
            id=1,
            ona_pk=59,
            organization=12,
            name='Project Zero'
        )

        serializer_data = ProjectSerializer(mocked_project).data

        expected_fields = {
            'id',
            'ona_pk',
            'organization',
            'last_updated',
            'name',
            'created',
            'modified',
            'deleted_at'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))

        self.assertEqual(59, serializer_data['ona_pk'])
        self.assertEqual(12, serializer_data['organization'])
        self.assertEqual('Project Zero', serializer_data['name'])
