# -*- coding: utf-8 -*-
"""
Test for Submission model
"""
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import six

from model_mommy import mommy
from tasking.utils import get_allowed_contenttypes


class TestSubmission(TestCase):
    """
    Test for Submission Model
    """

    def setUp(self):
        self.instance_type = get_allowed_contenttypes().filter(
            model='onainstance').first()

    def test_submission_model_str(self):
        """
        Test the string representation of Submission Model
        """
        cattle = mommy.make(
            'main.Task',
            name='Cattle Price')
        submission = mommy.make(
            'main.Submission',
            task=cattle,
            _fill_optional=['user', 'comment', 'submission_time'])
        expected = "Cattle Price - {} submission {}".format(
            submission.task.id, submission.id)
        self.assertEqual(expected, six.text_type(submission))

    def test_relationship_with_ona_instance(self):
        instance = mommy.make('ona.OnaInstance')
        cattle = mommy.make(
            'main.Task',
            name='Cattle Price')
        submission = mommy.make(
            'main.Submission',
            task=cattle,
            target_content_object=instance,
            _fill_optional=['user', 'comment', 'submission_time'])

        self.assertEqual(submission.target_object_id, instance.id)
        self.assertEqual(submission.target_content_type, self.instance_type)
