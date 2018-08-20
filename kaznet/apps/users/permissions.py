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


class IsAdmin(permissions.BasePermission):
    """
    Custom permissions class for Kaznet admin users
    """
    message = PERMISSION_MISSING

    def has_permission(self, request, view):
        """
        Checks that user in the request object is a Kaznet admin
        """
        return check_admin_permission(request)


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

        if view.action == 'list':
            ona_username = request.query_params.get('ona_username')
            if ona_username is not None:
                return (ona_username == request.user.userprofile.ona_username
                        or check_admin_permission(request))

        return check_admin_permission(request)

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user in the request object is linked to the
        Object
        """
        return request.user == obj.user or check_admin_permission(request)


class IsOwnSubmissionOrAdmin(permissions.BasePermission):
    """
    Custom permissions class for Kaznet users
    """
    message = PERMISSION_MISSING

    def has_permission(self, request, view):
        """
        Checks if the user is an Admin when trying to list
        """
        if view.action == 'list':
            user_params = request.query_params.get('user')
            if user_params is not None:
                user_params = int(user_params)
                return (user_params == request.user.id
                        or check_admin_permission(request))
        if view.action == 'retrieve':
            return True

        return check_admin_permission(request)

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user in the request is linked to the Object
        or if they are an admin
        """
        return request.user == obj.user or check_admin_permission(request)
