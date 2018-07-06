"""
Filters module for main Kaznet app
"""
from django_filters import rest_framework as filters

from kaznet.apps.main.models import Task, TaskOccurrence

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


class KaznetTaskOccurrenceFilterSet(filters.FilterSet):
    """
    Filterset for TaskOccurrence
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
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


class KaznetTaskFilterSet(filters.FilterSet):
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
        method='filter_timing'
    )

    # pylint: disable=too-few-public-methods
    class Meta(object):
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

        # filter_overrides = {
        #     models.DateTimeField: {
        #         'filter_class': filters.IsoDateTimeFilter
        #     },
        # }

    # pylint: disable=unused-argument
    def filter_timing(self, queryset, name, value):
        """
        Method to filter against task timing using TaskOccurrences
        """
        # get the filter
        try:
            the_filter = self.get_filters()[name]
        except KeyError:
            # this name isn't a valid filter
            return queryset

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
            # no data was found
            return queryset

        filter_args = {query_name: data}
        # get task ids
        # pylint: disable=no-member
        if name == 'modified':
            return queryset.filter(**filter_args)

        task_ids = TaskOccurrence.objects.filter(
            **filter_args).values_list('task_id', flat=True).distinct()
        return queryset.filter(id__in=task_ids)
