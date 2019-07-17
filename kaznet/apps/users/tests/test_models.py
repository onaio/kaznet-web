"""
Test for UserProfile model
"""
import random
import statistics
from datetime import datetime, timedelta
import pytz

from model_mommy import mommy
from rest_framework.authtoken.models import Token

from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.users.models import UserProfile
from kaznet.apps.main.models import Submission


class TestUserModels(MainTestBase):
    """
    Test class for User models
    """

    def setUp(self):
        super().setUp()

    def test_userprofile_model_creation(self):
        """
        Test that a UserProfile model is created when a User is created
        """
        user = mommy.make("auth.User", username="mosh")
        # assert that we have a userprofile object attached
        self.assertTrue(isinstance(user.userprofile, UserProfile))
        # check the username
        self.assertEqual("mosh", user.userprofile.user.username)
        # check the __str__ method on UserProfile
        self.assertEqual("mosh's profile", user.userprofile.__str__())

    def test_create_auth_token(self):
        """
        Test that auth token is created when user is created
        """
        user = mommy.make("auth.User", username="mosh")
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_submission_count(self):
        """
        Test that submission_count works
        """
        userprofile = mommy.make("auth.User").userprofile
        # make some submissions
        mommy.make("main.Submission", _quantity=789, user=userprofile.user)

        # user .objects so that we can get the submission count
        profile = UserProfile.objects.get(id=userprofile.id)

        self.assertEqual(789, profile.submission_count)

    def test_approved_submissions(self):
        """
        Test that the correct count of approved submissions is returned
        """
        userprofile = mommy.make("auth.User").userprofile

        mommy.make(
            "main.Submission",
            _quantity=200,
            user=userprofile.user,
            status=Submission.APPROVED,
        )
        mommy.make("main.Submission", _quantity=300, user=userprofile.user)

        self.assertEqual(userprofile.approved_submissions, 200)

    def test_rejected_submissions(self):
        """
        Test that the correct count of rejected submissions is returned
        """
        userprofile = mommy.make("auth.User").userprofile

        mommy.make(
            "main.Submission",
            _quantity=200,
            user=userprofile.user,
            status=Submission.REJECTED,
        )
        mommy.make("main.Submission", _quantity=300, user=userprofile.user)

        self.assertEqual(userprofile.rejected_submissions, 200)

    def test_approval_rate(self):
        """
        Test that the correct approval rate is returned
        """
        userprofile = mommy.make("auth.User").userprofile

        # when there are no submissions, the approval rate is 0
        self.assertEqual(userprofile.approval_rate, 0.0)

        approved_count = 200
        default_count = 300
        mommy.make(
            "main.Submission",
            _quantity=approved_count,
            user=userprofile.user,
            status=Submission.APPROVED,
        )
        mommy.make("main.Submission", _quantity=default_count,
                   user=userprofile.user)
        approval_rate = approved_count / (approved_count + default_count)

        # when there are submission
        self.assertEqual(userprofile.approval_rate, approval_rate)

    def test_amount_earned(self):
        """
        Test that the correct ammount earned is returned
        """
        userprofile = mommy.make("auth.User").userprofile
        bounty_ammount_sum = 0
        for _ in range(20):
            bounty = mommy.make("main.Bounty",
                                amount=random.randrange(100, 1000))
            bounty_ammount_sum += bounty.amount
            mommy.make(
                "main.Submission",
                user=userprofile.user,
                bounty=bounty,
                status=Submission.APPROVED,
            )
        # check if the submission gives the correct amount_earned
        self.assertEqual(userprofile.amount_earned.amount, bounty_ammount_sum)

    def get_datetime(self):
        """
        Generate a random datetime
        """
        # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
        min_year = 2018
        max_year = 2018
        start = datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)
        return start + (end - start) * random.random()

    def test_avg_submissions(self):
        """
        Test the average submissions property
        """
        userprofile = mommy.make("auth.User").userprofile
        submissions_per_month = [0] * 12

        for _ in range(1000):
            submission = mommy.make(
                "main.Submission",
                submission_time=self.get_datetime().replace(
                    tzinfo=pytz.timezone("Africa/Nairobi")
                ),
                user=userprofile.user,
                status=Submission.APPROVED,
            )
            submissions_per_month[submission.submission_time.month - 1] += 1

        self.assertEqual(
            userprofile.avg_submissions, statistics.mean(submissions_per_month)
        )

    def test_avg_approved_submissions(self):
        """
        Test the average approved submissions property
        """
        userprofile = mommy.make("auth.User").userprofile
        approved_submissions_per_month = [0] * 12

        for _ in range(1000):
            if random.choice([True, False]):
                submission = mommy.make(
                    "main.Submission",
                    submission_time=self.get_datetime().replace(
                        tzinfo=pytz.timezone("Africa/Nairobi")
                    ),
                    user=userprofile.user,
                    status=Submission.APPROVED,
                )
                approved_submissions_per_month[
                    submission.submission_time.month - 1
                ] += 1
            else:
                mommy.make(
                    "main.Submission",
                    submission_time=self.get_datetime().replace(
                        tzinfo=pytz.timezone("Africa/Nairobi")
                    ),
                    user=userprofile.user,
                )

        self.assertEqual(
            userprofile.avg_approved_submissions,
            statistics.mean(approved_submissions_per_month),
        )

    def test_avg_rejected_submissions(self):
        """
        Test the average rejected submissions property
        """
        userprofile = mommy.make("auth.User").userprofile
        rejected_submissions_per_month = [0] * 12

        for _ in range(1000):
            if random.choice([True, False]):
                submission = mommy.make(
                    "main.Submission",
                    submission_time=self.get_datetime().replace(
                        tzinfo=pytz.timezone("Africa/Nairobi")
                    ),
                    user=userprofile.user,
                    status=Submission.REJECTED,
                )
                rejected_submissions_per_month[
                    submission.submission_time.month - 1
                ] += 1
            else:
                mommy.make(
                    "main.Submission",
                    submission_time=self.get_datetime().replace(
                        tzinfo=pytz.timezone("Africa/Nairobi")
                    ),
                    user=userprofile.user,
                )

        self.assertEqual(
            userprofile.avg_rejected_submissions,
            statistics.mean(rejected_submissions_per_month),
        )

    def test_avg_amount_earned(self):
        """
        Test the average amount earned property
        """
        userprofile = mommy.make("auth.User").userprofile
        total_bounty_per_month = [0] * 12

        for _ in range(1000):
            bounty = mommy.make(
                "main.Bounty", amount=random.randrange(100, 1000))
            if random.choice([True, False]):
                submission = mommy.make(
                    "main.Submission",
                    submission_time=self.get_datetime().replace(
                        tzinfo=pytz.timezone("Africa/Nairobi")
                    ),
                    bounty=bounty,
                    user=userprofile.user,
                    status=Submission.APPROVED,
                )
                total_bounty_per_month[
                    submission.submission_time.month - 1
                ] += bounty.amount
            else:
                mommy.make(
                    "main.Submission",
                    submission_time=self.get_datetime().replace(
                        tzinfo=pytz.timezone("Africa/Nairobi")
                    ),
                    user=userprofile.user,
                    bounty=bounty,
                )

        self.assertEqual(
            userprofile.avg_amount_earned, statistics.mean(
                total_bounty_per_month)
        )

    def test_avg_approval_rate(self):
        """
        Test the average approval rate
        """
        userprofile = mommy.make("auth.User").userprofile
        approved_submissions_per_month = [0] * 12

        for _ in range(1000):
            if random.choice([True, False]):
                submission = mommy.make(
                    "main.Submission",
                    submission_time=self.get_datetime().replace(
                        tzinfo=pytz.timezone("Africa/Nairobi")
                    ),
                    user=userprofile.user,
                    status=Submission.APPROVED,
                )
                approved_submissions_per_month[
                    submission.submission_time.month - 1
                ] += 1
            else:
                mommy.make(
                    "main.Submission",
                    submission_time=self.get_datetime().replace(
                        tzinfo=pytz.timezone("Africa/Nairobi")
                    ),
                    user=userprofile.user,
                )
        approved = userprofile.avg_approved_submissions
        submissions = userprofile.avg_submissions
        avg_approval_rate = approved / submissions
        self.assertEqual(avg_approval_rate, userprofile.avg_approval_rate)
