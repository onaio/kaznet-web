"""
Main Tasks viewset module
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.main.common_tags import INCORRECT_CLONE_DATA
from kaznet.apps.main.filters import KaznetTaskFilterSet
from kaznet.apps.main.models import Task, TaskLocation
from kaznet.apps.main.serializers import KaznetTaskSerializer
from kaznet.apps.users.permissions import IsAdmin, IsAdminOrReadOnly


# pylint: disable=too-many-ancestors
class KaznetTaskViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Main Task Viewset class
    """
    authentication_classes = [
        SessionAuthentication, TokenAuthentication, OnaTempTokenAuthentication
    ]
    serializer_class = KaznetTaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter
    ]
    filter_class = KaznetTaskFilterSet
    search_fields = ['name']
    ordering_fields = [
        'created', 'modified', 'status', 'estimated_time', 'submission_count',
        'project__id', 'name', 'bounty__amount'
    ]
    queryset = Task.with_submission_count.all()

    # pylint: disable=unused-argument
    # pylint: disable=invalid-name
    @action(methods=['post'], detail=True, permission_classes=[IsAdmin])
    def clone_task(self, request, pk=None):
        """
        Action that clones a Task without it's XForms or
        Submissions
        """
        task_id = request.data.get('id')
        task = self.get_object()

        if task_id == str(task.id):
            # Get old Segment rules from Task
            segmentrules = task.segment_rules.all()
            # get task locations
            # pylint: disable=no-member
            task_locations = TaskLocation.objects.filter(task=task)

            # Get Bounty of Task
            bounty = task.bounty

            # clone it
            cloned_task = task
            cloned_task.pk = None
            cloned_task.target_content_type = None
            cloned_task.target_id = None
            cloned_task.name = f'{task.name} - Copy'
            cloned_task.save()

            # deal with segment rules
            cloned_task.segment_rules.set(segmentrules)

            # deal with locations
            for task_location in task_locations:
                task_location.id = None
                task_location.task = cloned_task
                task_location.save()

            # deal with bounty
            if bounty is not None:
                bounty.id = None
                bounty.task = cloned_task
                bounty.save()

            cloned_task.status = Task.DRAFT
            cloned_task.save()
            cloned_task_data = KaznetTaskSerializer(cloned_task).data
            return Response(cloned_task_data)
        return Response({'status': INCORRECT_CLONE_DATA})
