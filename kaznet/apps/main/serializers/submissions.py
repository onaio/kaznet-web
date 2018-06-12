"""
Main Submission Serializers
"""
from rest_framework_json_api import serializers
from tasking.serializers import SubmissionSerializer

from kaznet.apps.main.models import Submission


# pylint: disable=too-many-ancestors
class KaznetSubmissionSerializer(
        serializers.ModelSerializer, SubmissionSerializer):
    """
    Main Submission serializer class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for KaznetSubmissionSerializer
        """
        fields = [
            'id',
            'modified',
            'created',
            'task',
            'bounty',
            'location',
            'user',
            'submission_time',
            'valid',
            'approved',
            'status',
            'comments',
            'target_content_type',
            'target_id',
        ]

        model = Submission
