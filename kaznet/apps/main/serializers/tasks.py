"""
Main Tasks serializer module
"""
from dateutil.rrule import rrulestr
from rest_framework_json_api import serializers
from tasking.common_tags import INVALID_TIMING_RULE
from tasking.utils import get_rrule_end, get_rrule_start
from tasking.validators import validate_rrule

from kaznet.apps.main.models import Bounty, Task
from kaznet.apps.main.serializers.base import GenericForeignKeySerializer
from kaznet.apps.main.serializers.bounty import (BountySerializer,
                                                 SerializableAmountField)


# pylint: disable=too-many-ancestors
class KaznetTaskSerializer(GenericForeignKeySerializer):
    """
    Main Task Serializer class
    """
    start = serializers.DateTimeField(required=False)
    submission_count = serializers.SerializerMethodField()
    amount = SerializableAmountField(
        source='main.Bounty', required=False, write_only=True)
    total_bounty_payout = SerializableAmountField(read_only=True)
    current_bounty_amount = SerializableAmountField(read_only=True)
    bounty = BountySerializer(read_only=True)

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for KaznetTaskSerializer
        """
        fields = [
            'id',
            'created',
            'modified',
            'name',
            'amount',
            'parent',
            'estimated_time',
            'approved_submissions_count',
            'pending_submissions_count',
            'rejected_submissions_count',
            'total_bounty_payout',
            'current_bounty_amount',
            'required_expertise',
            'description',
            'xform_title',
            'status_display',
            'required_expertise_display',
            'client',
            'start',
            'end',
            'timing_rule',
            'total_submission_target',
            'user_submission_target',
            'status',
            'submission_count',
            'bounty',
            'target_content_type',
            'target_id',
            'segment_rules',
            'locations',
        ]

        model = Task

    def get_submission_count(self, obj):  # pylint: disable=no-self-use
        """
        Add a custom method to get submission count
        """
        try:
            return obj.submission_count
        except AttributeError:
            return obj.submissions

    # pylint: disable=no-self-use
    def validate_timing_rule(self, value):
        """
        Validate timing rule
        """
        if validate_rrule(value) is True:
            return value
        raise serializers.ValidationError(
            {'timing_rule': INVALID_TIMING_RULE}
        )

    def validate(self, attrs):
        """
        Object level validation method for TaskSerializer
        """

        # if timing_rule is provided, we extract start and end from its value
        if self.instance is not None:
            # we are doing an update
            timing_rule = attrs.get('timing_rule', self.instance.timing_rule)
        else:
            # we are creating a new object
            timing_rule = attrs.get('timing_rule')

        if timing_rule is not None:
            # get start and end values from timing_rule
            attrs['start'] = get_rrule_start(rrulestr(timing_rule))
            attrs['end'] = get_rrule_end(rrulestr(timing_rule))

        return super().validate(attrs)

    def create(self, validated_data):
        """
        Custom Create method to create Task then Bounty Object
        """
        amount = None

        try:
            amount = validated_data.pop('main')
        except KeyError:
            pass

        task = super().create(validated_data)

        if amount is not None:
            bounty_data = {
                'task': task,
                'amount': amount['Bounty']
            }

            BountySerializer.create(BountySerializer(),
                                    validated_data=bounty_data)

        return task

    def update(self, instance, validated_data):
        """
        Custom Update method for Task
        """
        amount = None

        try:
            amount = validated_data.pop('main')
        except KeyError:
            pass

        task = super().update(
            instance, validated_data)

        if amount is not None:
            try:
                task.bounty_set.get(amount=amount['Bounty'])
            # pylint: disable=no-member
            except Bounty.DoesNotExist:
                bounty_data = {
                    'task': task,
                    'amount': amount['Bounty']
                }
                BountySerializer.create(BountySerializer(),
                                        validated_data=bounty_data)
        return task
