# -*- coding: utf-8 -*-
"""
Filters Module for Users
"""
from rest_framework.filters import OrderingFilter


class UserProfileOrderingFilter(OrderingFilter):
    """
    Custom ordering class for UserProfiles
    """

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset
