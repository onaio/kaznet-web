"""
allauth_ona views module
"""
from django.conf import settings

import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2CallbackView,
                                                          OAuth2LoginView)

from .provider import OnadataProvider

BASE_URL = getattr(settings, 'ONA_BASE_URL', "https://api.ona.io")


class OnadataOAuth2Adapter(OAuth2Adapter):
    """
    Onadata OAuth2 adapter
    """
    provider_id = OnadataProvider.id
    access_token_url = f'{BASE_URL}/o/token/'
    authorize_url = f'{BASE_URL}/o/authorize/'
    profile_url = f'{BASE_URL}/api/v1/user.json'

    def complete_login(self, request, app, access_token, **kwargs):
        """
        Complete the login
        """
        headers = {'Authorization': f'Bearer {access_token.token}'}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)


# pylint: disable=invalid-name
oauth2_login = OAuth2LoginView.adapter_view(OnadataOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(OnadataOAuth2Adapter)
