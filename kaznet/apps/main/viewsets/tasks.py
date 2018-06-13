"""
Main Tasks viewset module
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.filters import KaznetTaskFilterSet
from kaznet.apps.main.models import Task
from kaznet.apps.main.serializers import KaznetTaskSerializer
from kaznet.apps.users.permissions import IsAdminOrReadOnly, IsAdmin


# pylint: disable=too-many-ancestors
class KaznetTaskViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Main Task Viewset class
    """
    serializer_class = KaznetTaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter]
    filter_class = KaznetTaskFilterSet
    search_fields = ['name']
    ordering_fields = [
        'created',
        'status',
        'estimated_time',
        'submission_count',
        'project__id',
        'name',
        'bounty__amount'
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
            # Get old Locations from Task
            locations = task.locations.all()
            # Get old Segment rules from Task
            segmentrules = task.segment_rules.all()
            # Get Bounty of Task
            bounty = task.bounty
            task.id = None
            task.pk = None
            task.target_content_type = None
            task.target_id = None
            task.name = f'{task.name} - Copy'
            task.save()
            task.locations.set(locations)
            task.segment_rules.set(segmentrules)

            if bounty is not None:
                bounty.id = None
                bounty.task = task
                bounty.save()

            task.status = 'd'
            task.save()
            task_data = KaznetTaskSerializer(task).data
            return Response(task_data)
        return Response({'status': 'Incorrect Data'})
