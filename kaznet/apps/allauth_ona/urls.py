"""
urls module for allauth_ona
"""
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import OnadataProvider

# pylint: disable=invalid-name
urlpatterns = default_urlpatterns(OnadataProvider)
