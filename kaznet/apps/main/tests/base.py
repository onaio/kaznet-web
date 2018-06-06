"""
Base Test class for main app
"""

from django.test import TestCase

from tasking.utils import get_allowed_contenttypes


class MainTestBase(TestCase):
    """
    Base test class
    """

    def setUp(self):
        """
        Setup tests
        """
        # get the content type for XForm model
        self.xform_type = get_allowed_contenttypes().filter(
            model='xform').first()
        # get the content type for Instance model
        self.instance_type = get_allowed_contenttypes().filter(
            model='instance').first()
        # get the content type for User model
        self.user_type = get_allowed_contenttypes().filter(
            model='user').first()