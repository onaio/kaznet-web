"""
Main Submissions ViewSet Module
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, renderers, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from django.http import StreamingHttpResponse
from django.conf import settings
from kaznet.apps.main.renderers import CSVStreamingRenderer
from kaznet.apps.main.authentication import OnaTempTokenAuthentication
from kaznet.apps.main.filters import KaznetSubmissionFilterSet
from kaznet.apps.main.models import Submission
from kaznet.apps.main.serializers import (KaznetSubmissionSerializer,
                                          SubmissionExportSerializer)
from kaznet.apps.users.permissions import IsOwnSubmissionOrAdmin


# pylint: disable=too-many-ancestors
class KaznetSubmissionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Submissions
    """
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        OnaTempTokenAuthentication
        ]
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
class SubmissionExportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Submission exports
    """
    authentication_classes = [
        TokenAuthentication,
        OnaTempTokenAuthentication,
        SessionAuthentication
    ]
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

        return super().list(request, *args, **kwargs)
