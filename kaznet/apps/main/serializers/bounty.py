"""
Bounty Serializer Module
"""

from rest_framework import serializers

from kaznet.apps.main.models import Bounty


class BountySerializer(serializers.ModelSerializer):
    """
    Client Serializer class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for ClientSerializer
        """

        fields = ['modified', 'task', 'amount', 'created', 'id']
        model = Bounty
