"""
Base test class for users tests
"""
from model_mommy import mommy

from kaznet.apps.users.models import UserProfile


def create_admin_user():
    """
    Return an admin role user
    """
    user = mommy.make('auth.User')
    user.userprofile.role = UserProfile.ADMIN
    user.userprofile.save()
    return user