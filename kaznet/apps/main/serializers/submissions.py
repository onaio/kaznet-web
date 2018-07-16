"""
Main Submission Serializers
"""
from rest_framework_json_api import serializers
from tasking.common_tags import CANT_EDIT_TASK

from kaznet.apps.main.models import Submission
from kaznet.apps.main.serializers.base import GenericForeignKeySerializer
from kaznet.apps.main.serializers.bounty import SerializableAmountField


# pylint: disable=too-many-ancestors
class KaznetSubmissionSerializer(GenericForeignKeySerializer):
    """
    Main Submission serializer class
    """
    amount = SerializableAmountField(read_only=True)

    # pylint: disable=too-few-public-methods
    class Meta:
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
            'amount'
        ]

        model = Submission

    def validate_task(self, value):
        """
        Validate Task
        """
        if self.instance is not None:
            if self.instance.task == value:
                return value
            else:
                raise serializers.ValidationError(
                    CANT_EDIT_TASK
                )
        else:
            return value
