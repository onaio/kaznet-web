"""
Mixins module
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from kaznet.apps.users.models import UserProfile


class ContributorNotAllowedMixin:  # pylint: disable=too-few-public-methods
    """
    This view mixin is used to prevent contributor-level users from
    accessing certain views.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Redirect the user to the contributor not allwed view
        if they are a contributor
        """
        if request.user.userprofile.role != UserProfile.ADMIN:
            return redirect(reverse("disallow_contributors"))
        return super().dispatch(request, *args, **kwargs)