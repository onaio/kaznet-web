"""
Celery tests module
"""
from kaznet.apps.main.tests.base import MainTestBase

from kaznet.celery import APP


class TestCelery(MainTestBase):
    """
    Tests Celery
    """

    def setUp(self):
        super().setUp()

    @APP.task(bind=True)
    def test_debug_task(self):
        """
        celery test
        """
        print(f'Request: {self.request}')
