"""
Main Submission Serializers
"""
from tasking.serializers import SubmissionSerializer

from kaznet.apps.main.models import Submission


# pylint: disable=too-many-ancestors
class KaznetSubmissionSerializer(SubmissionSerializer):
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
            'location',
            'user',
            'submission_time',
            'valid',
            'status',
            'comments',
            'target_content_type',
            'target_id',
        ]

        model = Submission
