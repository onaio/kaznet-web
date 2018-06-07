"""
Main Tasks serializer module
"""
from tasking.serializers import TaskSerializer

from kaznet.apps.main.models import Task
from kaznet.apps.main.serializers.bounty import (BountySerializer,
                                                 SerializableAmountField)
from kaznet.apps.main.models import Bounty


# pylint: disable=too-many-ancestors
class KaznetTaskSerializer(TaskSerializer):
    """
    Main Task Serializer class
    """

    amount = SerializableAmountField(source='main.Bounty', required=False)

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
            'description',
            'client',
            'start',
            'end',
            'timing_rule',
            'total_submission_target',
            'user_submission_target',
            'status',
            'submission_count',
            'target_content_type',
            'target_id',
            'segment_rules',
            'locations',
        ]

        model = Task

    def create(self, validated_data):
        """
        Custom Create method to create Task then Bounty Object
        """
        amount = None

        try:
            amount = validated_data.pop('main')
        except KeyError:
            pass

        task = super(KaznetTaskSerializer, self).create(validated_data)

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

        task = super(KaznetTaskSerializer, self).update(
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
