"""
Main Submission Serializers
"""
from rest_framework import serializers as drf_serializers
from rest_framework_json_api import serializers
from tasking.common_tags import CANT_EDIT_TASK

from kaznet.apps.main.common_tags import (LABEL_AMOUNT, LABEL_CURRENCY,
                                          LABEL_LOCATION, LABEL_PAYMENT_PHONE,
                                          LABEL_PHONE, LABEL_STATUS,
                                          LABEL_SUBMISSION_TIME, LABEL_TASK,
                                          LABEL_USER, LABEL_USER_ID, LABEL_LOCATION_ID,
                                          LABEL_TASK_ID)
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
    user = drf_serializers.SerializerMethodField(label=LABEL_USER)
    user_id = drf_serializers.SerializerMethodField(label=LABEL_USER_ID)
    task = drf_serializers.SerializerMethodField(label=LABEL_TASK)
    task_id = drf_serializers.SerializerMethodField(label=LABEL_TASK_ID)
    location = drf_serializers.SerializerMethodField(label=LABEL_LOCATION)
    location_id = drf_serializers.SerializerMethodField(
        label=LABEL_LOCATION_ID)
    submission_time = drf_serializers.SerializerMethodField(
        label=LABEL_SUBMISSION_TIME)
    amount = drf_serializers.SerializerMethodField(label=LABEL_AMOUNT)
    currency = drf_serializers.SerializerMethodField(label=LABEL_CURRENCY)
    status = drf_serializers.SerializerMethodField(label=LABEL_STATUS)
    phone_number = drf_serializers.SerializerMethodField(label=LABEL_PHONE)
    payment_number = drf_serializers.SerializerMethodField(
        label=LABEL_PAYMENT_PHONE)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for SubmissionExportSerializer
        """
        fields = [
            'id',
            'user',
            'user_id',
            'task',
            'task_id',
            'location',
            'location_id',
            'submission_time',
            'approved',
            'status',
            'comments',
            'amount',
            'currency',
            'phone_number',
            'payment_number',
        ]

        model = Submission

    def get_user(self, obj):  # pylint: disable=no-self-use
        """
        Get the user field
        """
        return obj.user.userprofile.get_name()

    def get_task(self, obj):  # pylint: disable=no-self-use
        """
        Get the task field
        """
        return obj.task.name

    def get_location(self, obj):  # pylint: disable=no-self-use
        """
        Get the location field
        """
        if obj.location:
            return obj.location.name
        return None

    def get_submission_time(self, obj):  # pylint: disable=no-self-use
        """
        Get the submission_time field
        """
        return obj.submission_time.isoformat()

    def get_amount(self, obj):  # pylint: disable=no-self-use
        """
        Get the amount field
        """
        if obj.amount:
            return obj.amount.amount
        return None

    def get_currency(self, obj):  # pylint: disable=no-self-use
        """
        Get the currency field
        """
        if obj.amount:
            return obj.amount.currency
        return None

    def get_status(self, obj):  # pylint: disable=no-self-use
        """
        Get the status field
        """
        return obj.status

    def get_phone_number(self, obj):  # pylint: disable=no-self-use
        """
        Get the phone_number field
        """
        if obj.user.userprofile.phone_number:
            return obj.user.userprofile.phone_number.as_e164
        return None

    def get_payment_number(self, obj):  # pylint: disable=no-self-use
        """
        Get the payment_number field
        """
        if obj.user.userprofile.payment_number:
            return obj.user.userprofile.payment_number.as_e164
        return None

    def get_user_id(self, obj):  #pylint: disable=no-self-use
        """
        Get the user_id field
        """
        return obj.user.id

    def get_task_id(self, obj):
        """
        Get the task_id
        """
        return obj.task.id

    def get_location_id(self, obj):
        """
        Get the task_id
        """
        return obj.location.id

