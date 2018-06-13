"""
KaznetContentType Serializer
"""
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers


class KaznetContentTypeSerializer(serializers.ModelSerializer):
    """
    Class for KaznetContentTypeSerializer
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for KaznetContentTypeSerializer
        """
        model = ContentType
        fields = [
            'id',
            'app_label',
            'model',
        ]
