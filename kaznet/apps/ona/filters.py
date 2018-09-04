"""
Filters module for ona Kaznet app
"""
from django_filters import rest_framework as filters

from kaznet.apps.main.models import Task
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
    class Meta:
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
        # get ids of XForms that have task attachments

        # pylint: disable=no-member
        form_ids = Task.objects.filter(
            target_content_type__model='xform').values_list(
                'target_object_id', flat=True)

        # ensure the list has no None values as this ruins the queryset
        # statements below
        form_ids = [_ for _ in form_ids if _ is not None]

        if value is True:
            return queryset.filter(id__in=form_ids)

        return queryset.exclude(id__in=form_ids)
