"""
Client Serializer Module
"""

from rest_framework_json_api import serializers

from kaznet.apps.main.models import Client


# pylint: disable=too-many-ancestors
class ClientSerializer(serializers.ModelSerializer):
    """
    Client Serializer class
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for ClientSerializer
        """

        fields = ['name', 'id', 'created']
        model = Client
