"""
Bounty Serializer Module
"""

from django.conf import settings

from django_prices.models import Money
from rest_framework_json_api import serializers

from kaznet.apps.main.models import Bounty


def create_bounty(task, amount):
    """
    Create a bounty object
    """
    # then create the bounty object
    if amount is not None:
        bounty_data = {
            'task': task,
            'amount': amount
        }

        return BountySerializer.create(
            BountySerializer(), validated_data=bounty_data)

    return None


class SerializableAmountField(serializers.Field):
    """
    Custom Field for Amount
    """

    def to_representation(self, value):
        """
        Custom to representation for Serializable amount field
        """
        return f'{value.amount} {value.currency}'

    def to_internal_value(self, data):
        """
        Custom to_internal_value for SerializableAmountField
        """
        return Money(data, settings.KAZNET_DEFAULT_CURRENCY)


# pylint: disable=too-many-ancestors
class BountySerializer(serializers.ModelSerializer):
    """
    Client Serializer class
    """

    amount = SerializableAmountField()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for ClientSerializer
        """

        fields = ['modified', 'task', 'amount', 'created', 'id']
        model = Bounty
