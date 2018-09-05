"""
Kaznet main app views module
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class ReactAppView(LoginRequiredMixin, TemplateView):
    """
    This views is meant to serve as the frontend react app content
    https://github.com/onaio/kaznet-frontend
    """
    template_name = "index.html"