"""
Base test class for users tests
"""
from datetime import datetime, timedelta
import random
from model_mommy import mommy
import pytz

from kaznet.apps.users.models import UserProfile


def create_admin_user():
    """
    Return an admin role user
    """
    user = mommy.make(
        'auth.User', first_name='Ona', last_name='Kenya')
    user.userprofile.role = UserProfile.ADMIN
    user.userprofile.save()
    return user


def get_datetime():
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


def generate_submissions(userprofile, approve_or_reject):
    """
    Generate 1000 submissions for the supplied userprofile
    """
    for _ in range(1000):
        bounty = mommy.make(
            "main.Bounty", amount=random.randrange(100, 1000))
        if random.choice([True, False]):
            mommy.make(
                "main.Submission",
                submission_time=get_datetime().replace(
                    tzinfo=pytz.timezone("Africa/Nairobi")
                ),
                bounty=bounty,
                user=userprofile.user,
                status=approve_or_reject,
            )
        else:
            mommy.make(
                "main.Submission",
                submission_time=get_datetime().replace(
                    tzinfo=pytz.timezone("Africa/Nairobi")
                ),
                bounty=bounty,
                user=userprofile.user,
            )
