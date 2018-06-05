# -*- coding: utf-8 -*-
"""
Test for Task model
"""
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import six

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
        self.assertEqual(expected, six.text_type(cow_price))

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
