"""
Test module for BountySerializer
"""
from django.test import TestCase

from django_prices.models import Money
from model_mommy import mommy

from kaznet.apps.main.serializers import BountySerializer


class TestBountySerializer(TestCase):
    """
    Test the ClientSerializer
    """

    def test_create_bounty(self):
        """
        Test that serializer can create a bounty
        """

        mocked_task = mommy.make('main.Task')

        data = {
            "task": mocked_task.id,
            "amount": '5400.00'
        }

        serializer_instance = BountySerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        bounty = serializer_instance.save()

        # Serializer Changes the amount
        data['amount'] = '5400.00 KES'

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual(bounty.task, mocked_task)
        self.assertEqual(bounty.amount, Money('5400', 'KES'))

        expected_fields = ['task', 'id', 'amount', 'modified', 'created']
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
