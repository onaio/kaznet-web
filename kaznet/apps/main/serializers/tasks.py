"""
Main Tasks serializer module
"""
from django.utils import timezone

from dateutil.rrule import rrulestr
from rest_framework_json_api import serializers
from tasking.common_tags import (INVALID_END_DATE, INVALID_START_DATE,
                                 INVALID_TIMING_RULE)
from tasking.utils import get_rrule_end, get_rrule_start
from tasking.validators import validate_rrule

from kaznet.apps.main.models import Bounty, Task, TaskLocation
from kaznet.apps.main.serializers import (TaskLocationCreateSerializer,
                                          TaskLocationSerializer)
from kaznet.apps.main.serializers.base import GenericForeignKeySerializer
from kaznet.apps.main.serializers.bounty import (BountySerializer,
                                                 SerializableAmountField,
                                                 create_bounty)


# pylint: disable=too-many-ancestors
class KaznetTaskSerializer(GenericForeignKeySerializer):
    """
    Main Task Serializer class
    """
    start = serializers.DateTimeField(required=False)
    submission_count = serializers.SerializerMethodField()
    amount = SerializableAmountField(
        source='bounty', required=False, write_only=True)
    total_bounty_payout = SerializableAmountField(read_only=True)
    current_bounty_amount = SerializableAmountField(read_only=True)
    bounty = BountySerializer(read_only=True)
    locations_input = TaskLocationCreateSerializer(
        many=True, required=False, write_only=True)
    task_locations = serializers.SerializerMethodField(read_only=True)

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for KaznetTaskSerializer
        """
        fields = [
            'id',
            'created',
            'created_by',
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
            'xform_id_string',
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
            'created_by_name'
            'locations_input',
            'task_locations',
        ]
        model = Task
        read_only_fields = ['locations', 'created_by', 'created_by_name']

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
        if value is not None:
            if validate_rrule(value) is True:
                return value
            raise serializers.ValidationError(
                {'timing_rule': INVALID_TIMING_RULE}
            )
        return None

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
            end_time = attrs.get('end')
            attrs['start'] = get_rrule_start(rrulestr(timing_rule))
            # If the user did not set the end_time and passed the timing_rule
            # We try to set the end_date to the timing rules end
            if end_time is None:
                attrs['end'] = get_rrule_end(rrulestr(timing_rule))

        target_id = attrs.get('target_object_id')
        end_date = attrs.get('end')
        start_date = attrs.get('start')

        # If end date is present we validate that it is greater than start_date
        if end_date is not None:
            # If end date is lesser than the start date raise an error
            if end_date < start_date:
                raise serializers.ValidationError(
                    {'end': INVALID_END_DATE, 'start': INVALID_START_DATE}
                )

        if start_date > timezone.now():
            attrs['status'] = Task.SCHEDULED

        if target_id is None:
            attrs['status'] = Task.DRAFT

        return super().validate(attrs)

    def get_task_locations(self, obj):
        """
        Get serialized TaskLocation objects
        """
        # pylint: disable=no-member
        queryset = TaskLocation.objects.filter(task=obj)
        return TaskLocationSerializer(queryset, many=True).data

    def create(self, validated_data):
        """
        Custom Create method for Task
        """
        # get current user and set that as created_by
        try:
            request = self.context['request']
        except KeyError:
            pass
        else:
            if request is not None:
                user = getattr(request, 'user', None)
                if user.is_authenticated:
                    validated_data['created_by'] = user

        # get the supplied amount
        try:
            amount = validated_data.pop('bounty')
        except KeyError:
            amount = None

        # create the task
        task = super().create(validated_data)

        # create the bounty object
        create_bounty(task, amount)

        return task

    def update(self, instance, validated_data):
        """
        Custom Update method for Task
        """
        # get the supplied amount
        try:
            amount = validated_data.pop('bounty')
        except KeyError:
            amount = None

        # update the task
        task = super().update(instance, validated_data)

        # create the bounty object
        create_bounty(task, amount)

        return task
