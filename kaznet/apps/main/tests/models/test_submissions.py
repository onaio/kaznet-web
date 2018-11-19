"""
Test for Submission model
"""

from model_mommy import mommy
from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.tests.base import MainTestBase


class TestSubmission(MainTestBase):
    """
    Test for Submission Model
    """

    def setUp(self):
        super().setUp()

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
