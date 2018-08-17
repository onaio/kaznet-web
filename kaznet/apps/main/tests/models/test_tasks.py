# -*- coding: utf-8 -*-
"""
Test for Task model
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy
from tasking.utils import get_allowed_contenttypes


class TestTasks(TestCase):
    """
    Test class for task models
    """

    def setUp(self):
        self.instance_type = get_allowed_contenttypes().filter(
            model='xform').first()

    def test_task_model_str(self):
        """
        Test the str method on Task model
        """
        cow_price = mommy.make('main.Task', name="Cow prices")
        expected = 'Cow prices - {}'.format(cow_price.pk)
        self.assertEqual(expected, str(cow_price))

    def test_create_task_from_xform(self):
        """
        For every ona xform a signal is triggered to create
        a corresponding kaznet task
        """
        xform = mommy.make('ona.XForm')
        cattle_task = mommy.make(
            'main.Task',
            name='Cattle Price',
            target_content_object=xform
        )

        self.assertEqual(cattle_task.target_object_id, xform.id)
        self.assertEqual(cattle_task.target_content_type, self.instance_type)

    def test_created_by_name(self):
        """
        Test the `created_by_name` property
        """
        cate_user = mommy.make(
            'auth.User', username='cate', first_name='Cate', last_name='Doe')
        self.assertEqual(
            'Cate Doe',
            mommy.make('main.Task', created_by=cate_user).created_by_name
        )

    def test_task_xform(self):
        """
        Test:
            - get_xform method
            - get_xform_title method
            - get_xform_id_string method
            - xform_title property
            - xform_id_string property
        """
        xform = mommy.make(
            'ona.XForm',
            title='Coconut',
            id_string='coconut828',
            ona_pk=200,
            ona_project_id=12389)
        # test when no xform
        task_no_xform = mommy.make('main.Task')
        self.assertEqual(None, task_no_xform.get_xform())
        self.assertEqual(None, task_no_xform.get_xform_title())
        self.assertEqual(None, task_no_xform.get_xform_id_string())
        self.assertEqual(None, task_no_xform.xform_title)
        self.assertEqual(None, task_no_xform.xform_id_string)
        # test when XForm
        task = mommy.make('main.Task', target_content_object=xform)
        self.assertEqual(xform, task.get_xform())
        self.assertEqual('Coconut', task.get_xform_title())
        self.assertEqual('coconut828', task.get_xform_id_string())
        self.assertEqual('Coconut', task.xform_title)
        self.assertEqual(200, task.xform_ona_id)
        self.assertEqual('coconut828', task.xform_id_string)
        self.assertEqual(12389, task.xform_project_id)
