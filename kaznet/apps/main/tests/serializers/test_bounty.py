"""
Test module for BountySerializer
"""
from django.test import TestCase

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

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual(bounty.task, mocked_task)
        self.assertEqual(bounty.amount, 5400.00)

        expected_fields = ['task', 'id', 'amount', 'modified', 'created']
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
