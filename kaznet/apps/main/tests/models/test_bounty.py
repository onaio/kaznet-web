"""
Test for Bounty model
"""
from django.test import TestCase
from model_mommy import mommy


class TestBounty(TestCase):
    """
    Test class for Bounty mdoels
    """

    def test_bounty_str(self):
        """
        Test Bounty String Representation
        """
        amount = 5000
        kitten_prices = mommy.make('main.Task', name="kitten prices")
        bounty = mommy.make('main.Bounty', task=kitten_prices, amount=amount)

        expected = f"Task {kitten_prices.id} bounty is {amount}"
        self.assertEqual(expected, bounty.__str__())
