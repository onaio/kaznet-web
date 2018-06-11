"""
auth_ona views module
"""
from django.conf import settings

import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2CallbackView,
                                                          OAuth2LoginView)

from kaznet.appa.auth_ona.provider import OnadataProvider

BASE_URL = getattr(settings, 'ONA_BASE_URL', "https://api.ona.io")


class OnadataOAuth2Adapter(OAuth2Adapter):
    """
    Onadata OAuth2 adapter
    """
    provider_id = OnadataProvider.id
    access_token_url = '{BASE_URL}/authorization/token?type=web_server'
    authorize_url = '{BASE_URL}/authorization/new'
    profile_url = '{BASE_URL}/authorization.json'

    def complete_login(self, request, app, token, **kwargs):
        """
        Complete the login
        """
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)


oauth2_login = OAuth2LoginView.adapter_view(OnadataOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(OnadataOAuth2Adapter)
