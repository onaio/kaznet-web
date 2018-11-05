"""
Test for Bounty model
"""
from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase


class TestBounty(MainTestBase):
    """
    Test class for Bounty mdoels
    """

    def setUp(self):
        super().setUp()

    def test_bounty_str(self):
        """
        Test Bounty String Representation
        """
        amount = 5000
        kitten_prices = mommy.make('main.Task', name="kitten prices")
        bounty = mommy.make('main.Bounty', task=kitten_prices, amount=amount)

        expected = f"Task {kitten_prices.id} bounty is {amount}"
        self.assertEqual(expected, bounty.__str__())
