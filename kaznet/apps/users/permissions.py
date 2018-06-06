"""
Kaznet users permissions module
"""
from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions
from kaznet.apps.users.models import UserProfile


class AdminUserPermission(permissions.BasePermission):
    """
    Custom permissions class for Kaznet admin users
    """
    message = _('You shall not pass.')

    def has_permission(self, request, view):
        """
        Checks if the user in the request object is a Kaznet admin
        """
        try:
            return request.user.userprofile.role == UserProfile.ADMIN
        except AttributeError:
            pass

        return False
