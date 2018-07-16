"""
Init module for main viewsets
"""
from kaznet.apps.main.viewsets.tasks import KaznetTaskViewSet  # noqa
from kaznet.apps.main.viewsets.client import ClientViewSet  # noqa
from kaznet.apps.main.viewsets.locations import KaznetLocationViewSet  # noqa
from kaznet.apps.main.viewsets.occurences import KaznetTaskOccurrenceViewSet  # noqa
from kaznet.apps.main.viewsets.bounty import BountyViewSet  # noqa
from kaznet.apps.main.viewsets.submissions import KaznetSubmissionsViewSet  # noqa
from kaznet.apps.main.viewsets.contenttype import ContentTypeViewSet  # noqa
from kaznet.apps.main.viewsets.locationtypes import KaznetLocationTypeViewSet  # noqa
