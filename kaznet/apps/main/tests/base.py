"""
Base Test class for main app
"""

from django.db.models import signals
from django.test import TestCase

from kaznet.apps.ona.models import XForm
from tasking.utils import get_allowed_contenttypes


class MainTestBase(TestCase):
    """
    Base test class
    """

    def setUp(self):
        """
        Setup tests
        """
        super().setUp()
        # get the content type for XForm model
        self.xform_type = get_allowed_contenttypes().filter(
            model='xform').first()
        # get the content type for Instance model
        self.instance_type = get_allowed_contenttypes().filter(
            model='instance').first()
        # get the content type for User model
        self.user_type = get_allowed_contenttypes().filter(
            model='user').first()

        # disconnect signals
        signals.post_save.disconnect(
            sender=XForm, dispatch_uid="auto_create_ona_filtered_data_sets")
        signals.post_save.disconnect(
            sender=XForm, dispatch_uid="create_form_webhook_signal")
