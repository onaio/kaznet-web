"""
Init module for main serializers
"""
from kaznet.apps.main.serializers.bounty import BountySerializer  # noqa
from kaznet.apps.main.serializers.client import ClientSerializer  # noqa
from kaznet.apps.main.serializers.contenttype import KaznetContentTypeSerializer  # noqa
from kaznet.apps.main.serializers.locations import KaznetLocationSerializer  # noqa
from kaznet.apps.main.serializers.occurences import KaznetTaskOccurrenceSerializer  # noqa
from kaznet.apps.main.serializers.submissions import KaznetSubmissionSerializer  # noqa
from kaznet.apps.main.serializers.task_location import (TaskLocationCreateSerializer,  # noqa
                                                        TaskLocationSerializer)
from kaznet.apps.main.serializers.tasks import KaznetTaskSerializer  # noqa
