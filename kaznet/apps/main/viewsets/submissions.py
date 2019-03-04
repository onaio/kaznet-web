"""
Main Submissions ViewSet Module
"""

from django.conf import settings
from django.http import StreamingHttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, renderers, viewsets
from rest_framework.permissions import IsAuthenticated

from kaznet.apps.main.filters import KaznetSubmissionFilterSet
from kaznet.apps.main.mixins import KaznetViewsetMixin
from kaznet.apps.main.models import Submission
from kaznet.apps.main.renderers import CSVStreamingRenderer
from kaznet.apps.main.serializers import (KaznetSubmissionSerializer,
                                          SubmissionExportSerializer)
from kaznet.apps.users.permissions import IsOwnSubmissionOrAdmin


# pylint: disable=too-many-ancestors
class KaznetSubmissionsViewSet(
        KaznetViewsetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Submissions
    """
    serializer_class = KaznetSubmissionSerializer
    permission_classes = [IsAuthenticated, IsOwnSubmissionOrAdmin]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_class = KaznetSubmissionFilterSet
    ordering_fields = [
        'bounty__amount',
        'submission_time',
        'task__id',
        'modified'
    ]
    queryset = Submission.objects.all()  # pylint: disable=no-member


# pylint: disable=too-many-ancestors
class SubmissionExportViewSet(
        KaznetViewsetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Submission exports
    """
    serializer_class = SubmissionExportSerializer
    permission_classes = [IsAuthenticated, IsOwnSubmissionOrAdmin]
    renderer_classes = [
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        CSVStreamingRenderer,
    ]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_class = KaznetSubmissionFilterSet
    ordering_fields = [
        'submission_time',
        'task__id',
    ]
    queryset = Submission.objects.all()  # pylint: disable=no-member

    def list(self, request, *args, **kwargs):
        """
        Custom list action to enable streaming
        """
        if request.GET.get('format') == 'csv':
            renderer = CSVStreamingRenderer()
            queryset = self.filter_queryset(self.get_queryset())

            response = StreamingHttpResponse(
                renderer.render({
                    'queryset': queryset,
                    'serializer': self.serializer_class,
                    'context': {'request': request},
                }), content_type='text/csv')

            filename = settings.EXPORT_FILENAME

            response['Content-Disposition'] = \
                f'attachment; filename="{filename}.csv"'

            return response

        # pylint: disable=no-member
        return super().list(request, *args, **kwargs)
