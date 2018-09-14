"""
Kaznet main app views module
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from kaznet.apps.main.mixins import ContributorNotAllowedMixin


class ReactAppView(
        LoginRequiredMixin, ContributorNotAllowedMixin, TemplateView):
    """
    This views is meant to serve as the frontend react app content
    https://github.com/onaio/kaznet-frontend
    """
    template_name = "index.html"


class ContributorNotAllowed(LoginRequiredMixin, TemplateView):
    """
    This is the view that contributor-level users will be redirected to
    because they are not (yet) allowed to access the ReactAppView
    """
    template_name = "contributor-not-allowed.html"
