"""
Main Submission Serializers
"""
from rest_framework import serializers as drf_serializers
from rest_framework_json_api import serializers
from tasking.common_tags import CANT_EDIT_TASK

from kaznet.apps.main.common_tags import (LABEL_AMOUNT, LABEL_LOCATION,
                                          LABEL_PAYMENT_PHONE, LABEL_PHONE,
                                          LABEL_STATUS, LABEL_SUBMISSION_TIME,
                                          LABEL_TASK, LABEL_USER)
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

            raise serializers.ValidationError(
                CANT_EDIT_TASK
            )

        return value


class SubmissionExportSerializer(drf_serializers.ModelSerializer):
    """
    Serializer class used for Sumission exports
    """
    user = serializers.SerializerMethodField(label=LABEL_USER)
    task = serializers.SerializerMethodField(label=LABEL_TASK)
    location = serializers.SerializerMethodField(label=LABEL_LOCATION)
    submission_time = serializers.SerializerMethodField(
        label=LABEL_SUBMISSION_TIME)
    amount = serializers.SerializerMethodField(label=LABEL_AMOUNT)
    status = serializers.SerializerMethodField(label=LABEL_STATUS)
    phone_number = serializers.SerializerMethodField(label=LABEL_PHONE)
    payment_number = serializers.SerializerMethodField(
        label=LABEL_PAYMENT_PHONE)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for SubmissionExportSerializer
        """
        fields = [
            'id',
            'user',
            'task',
            'location',
            'submission_time',
            'approved',
            'status',
            'comments',
            'amount',
            'phone_number',
            'payment_number',
        ]

        model = Submission

    def get_user(self, obj):
        """
        Get the user field
        """
        return obj.user.userprofile.get_name()

    def get_task(self, obj):
        """
        Get the task field
        """
        return obj.task.name

    def get_location(self, obj):
        """
        Get the location field
        """
        if obj.location:
            return obj.location.name

    def get_submission_time(self, obj):
        """
        Get the submission_time field
        """
        return obj.submission_time.isoformat()

    def get_amount(self, obj):
        """
        Get the amount field
        """
        if obj.amount:
            return f'{obj.amount.amount} {obj.amount.currency}'

    def get_status(self, obj):
        """
        Get the status field
        """
        return obj.status

    def get_phone_number(self, obj):
        """
        Get the phone_number field
        """
        if obj.user.userprofile.phone_number:
            return obj.user.userprofile.phone_number.as_e164

    def get_payment_number(self, obj):
        """
        Get the payment_number field
        """
        if obj.user.userprofile.payment_number:
            return obj.user.userprofile.payment_number.as_e164
