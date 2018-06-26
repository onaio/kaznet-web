"""
Filters module for ona Kaznet app
"""
from django.db.models import Case, IntegerField, Value, When

from django_filters import rest_framework as filters

from kaznet.apps.ona.models import XForm


class XFormFilterSet(filters.FilterSet):
    """
    Filterset for XForm
    """
    has_task = filters.BooleanFilter(
        name='has_task',
        method='filter_has_task'
    )

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for XFormFilterSet
        """
        model = XForm
        fields = ['has_task']

    def filter_has_task(self, queryset, name, value):
        """
        Method to filter has_task
        """
        return queryset.annotate(task_present=Case(
            When(task=None, then=Value(0)), default=Value(1),
            output_field=IntegerField()
            )).filter(task_present=value)
