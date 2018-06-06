"""
Kaznet users permissions module
"""
from rest_framework import permissions

from kaznet.apps.users.common_tags import PERMISSION_MISSING
from kaznet.apps.users.models import UserProfile


def check_admin_permission(request: object):
    """
    Checks if the user sending a request is an Admin
    """
    try:
        return request.user.userprofile.role == UserProfile.ADMIN
    except AttributeError:
        pass

    return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permissions class for Kaznet admin users
    """
    message = PERMISSION_MISSING

    def has_permission(self, request, view):
        """
        Checks if the user in the request object is a Kaznet admin
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return check_admin_permission(request)


class IsOwnUserProfileOrAdmin(permissions.BasePermission):
    """
    Custom permissions class for Kaznet users
    """
    message = PERMISSION_MISSING

    def has_permission(self, request, view):
        """
        Checks if the user is an Admin when trying to list
        """
        if view.action in ['retrieve', 'partial_update']:
            return True
        return check_admin_permission(request)

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user in the request object is linked to the
        Object
        """
        return request.user == obj.user or check_admin_permission(request)
