"""
Filters module for ona Kaznet app
"""
from django.db.models import Case, BooleanField, When

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

    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def filter_has_task(self, queryset, name, value):
        """
        Method to filter has_task
        """
        return queryset.annotate(task_present=Case(
            When(task=None, then=False), default=True,
            output_field=BooleanField()
            )).filter(task_present=value)
