# -*- coding: utf-8 -*-
"""
Test for Submission model
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy
from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.models import Submission


class TestSubmission(TestCase):
    """
    Test for Submission Model
    """

    def setUp(self):
        self.instance_type = get_allowed_contenttypes().filter(
            model='instance').first()

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
        self.assertEqual(expected, str(submission))

    def test_relationship_with_ona_instance(self):
        """
        Test the link between a submission and an ona instance
        """
        instance = mommy.make('ona.Instance')
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

    def test_submissions_have_bounties(self):
        """
        Test Link Between Bounties and Submissions
        """
        cattle = mommy.make(
            'main.Task',
            name='Cattle Price')
        bounty_instance = mommy.make(
            'main.Bounty',
            task=cattle)
        submission = mommy.make(
            'main.Submission',
            task=cattle,
            bounty=bounty_instance,
            _fill_optional=['user', 'comment', 'submission_time'])

        self.assertEqual(submission.bounty.id, bounty_instance.id)

    def test_submission_approved(self):
        """
        Test that the approved property works
        """

        submission = mommy.make(
            'main.Submission',
            status=Submission.APPROVED
            )

        self.assertTrue(submission.approved)

    def test_submission_amount(self):
        """
        Test the amount property gets the correct Bounty
        Amount
        """
        cattle = mommy.make(
            'main.Task',
            name='Cattle Price')
        bounty_instance = mommy.make(
            'main.Bounty',
            amount=4000,
            task=cattle)
        submission = mommy.make(
            'main.Submission',
            task=cattle,
            bounty=bounty_instance,
            _fill_optional=['user', 'comment', 'submission_time'])

        self.assertEqual(submission.amount, 4000)
