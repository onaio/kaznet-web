"""
Celery tests module
"""
from django.test import TestCase

from kaznet.celery import APP


class TestCelery(TestCase):
    """
    Tests Celery
    """

    @APP.task(bind=True)
    def test_debug_task(self):
        """
        celery test
        """
        print(f'Request: {self.request}')
