"""
Filters module for main Kaznet app
"""
from django_filters import rest_framework as filters

from kaznet.apps.main.models import Task, TaskOccurrence, Location, Submission
from kaznet.apps.users.models import UserProfile

DATE_LOOKUPS = [
    'exact', 'gt', 'lt', 'gte', 'lte', 'year', 'year__gt', 'year__lt',
    'year__gte', 'year__lte', 'month', 'month__gt', 'month__lt',
    'month__gte', 'month__lte', 'day', 'day__gt', 'day__lt', 'day__gte',
    'day__lte']

DATETIME_LOOKUPS = [
    'exact', 'gt', 'lt', 'gte', 'lte', 'date', 'date__gt', 'date__lt',
    'date__gte', 'date__lte', 'time', 'time__gt', 'time__lt', 'time__gte',
    'time__lte'
]
TIME_LOOKUPS = ['exact', 'gt', 'lt', 'gte', 'lte']


class KaznetFilterSet(filters.FilterSet):
    """
    Generic filterset class for Kaznet
    """

    def _get_filter_args(self, name):
        """
        This method returns lookups-aware filter arguments
        """
        # get the filter
        try:
            the_filter = self.get_filters()[name]
        except KeyError:
            # this name isn't a valid filter
            return None

        # first try the exact name
        data = self.data.get(name)
        if data is not None:
            query_name = name
        else:
            # get the lookups
            lookups = the_filter.lookup_expr
            # loop through lookups to find which one is being used
            if lookups:
                for lookup in lookups:
                    query_name = self.get_filter_name(name, lookup)
                    data = self.data.get(query_name)
                    if data is not None:
                        break

        if data is None:
            return None

        return {query_name: data}

    # pylint: disable=unused-argument
    def filter_modified(self, queryset, name, value):
        """
        Filter by modified
        """
        filter_args = self._get_filter_args(name)

        if filter_args is None:
            return queryset

        return queryset.filter(**filter_args)


class KaznetLocationFilterSet(KaznetFilterSet):
    """
    Filterset for locations
    """
    modified = filters.DateTimeFilter(
        name='modified',
        lookup_expr=DATETIME_LOOKUPS,
        method='filter_modified'
    )

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for KaznetLocationFilterSet
        """
        model = Location
        fields = [
            'parent',
            'country',
            'modified',
        ]


class KaznetTaskOccurrenceFilterSet(filters.FilterSet):
    """
    Filterset for TaskOccurrence
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskOccurrenceFilterSet
        """
        model = TaskOccurrence
        fields = {
            'task': ['exact'],
            'date': DATE_LOOKUPS,
            'start_time': TIME_LOOKUPS,
            'end_time': TIME_LOOKUPS
        }


class KaznetTaskFilterSet(KaznetFilterSet):
    """
    Filterset for Task
    """
    date = filters.DateFilter(
        name='date',
        lookup_expr=DATE_LOOKUPS,
        method='filter_timing'
    )
    start_time = filters.TimeFilter(
        name='start_time',
        lookup_expr=TIME_LOOKUPS,
        method='filter_timing'
    )
    end_time = filters.TimeFilter(
        name='end_time',
        lookup_expr=TIME_LOOKUPS,
        method='filter_timing'
    )
    modified = filters.DateTimeFilter(
        name='modified',
        lookup_expr=DATETIME_LOOKUPS,
        method='filter_modified'
    )

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskFilterSet
        """
        model = Task
        fields = [
            'locations',
            'modified',
            'status',
            'project',
            'parent',
            'client',
            'date',
            'start_time',
            'end_time'
        ]

    # pylint: disable=unused-argument
    def filter_timing(self, queryset, name, value):
        """
        Method to filter against task timing using TaskOccurrences
        """
        filter_args = self._get_filter_args(name)

        if filter_args is None:
            return queryset

        # get task ids
        # pylint: disable=no-member
        task_ids = TaskOccurrence.objects.filter(
            **filter_args).values_list('task_id', flat=True).distinct()
        return queryset.filter(id__in=task_ids)


class KaznetSubmissionFilterSet(KaznetFilterSet):
    """
    Filterset for submissions
    """
    modified = filters.DateTimeFilter(
        name='modified',
        lookup_expr=DATETIME_LOOKUPS,
        method='filter_modified'
    )
    userprofile = filters.ModelChoiceFilter(
        name='user__userprofile',
        queryset=UserProfile.objects.all()
    )

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for KaznetSubmissionFilterSet
        """
        model = Submission
        fields = [
            'task',
            'user',
            'userprofile',
            'status',
            'location',
            'valid',
            'modified',
            'submission_time',
        ]
