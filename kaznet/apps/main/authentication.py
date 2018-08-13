"""
Custom Authentication Module
"""
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache

from rest_framework import exceptions
from rest_framework.authentication import (TokenAuthentication,
                                           get_authorization_header)

from kaznet.apps.main.common_tags import (AUTH_USER_DOESNT_EXIST,
                                          AUTH_USER_NOT_LOGGED_IN,
                                          INVALID_TOKEN_CREDENTIALS_MISSING,
                                          INVALID_TOKEN_SPACES_CONTAINED)
from kaznet.apps.ona.api import request_session
from kaznet.apps.users.models import UserProfile


class OnaTempTokenAuthentication(TokenAuthentication):
    """
    Custom Authentication that authenticates a User Using the OnaData
    User Endpoint
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != 'temptoken':
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                INVALID_TOKEN_CREDENTIALS_MISSING)
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(
                INVALID_TOKEN_SPACES_CONTAINED)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        validation_endpoint = urljoin(
            settings.ONA_BASE_URL, 'api/v1/user')
        username = cache.get(key)
        cached = False

        if username is None:
            response = request_session(
                validation_endpoint,
                'GET',
                headers={'Authorization': f'TempToken ${key}'}
                )

            if response.status_code != 200:
                raise exceptions.AuthenticationFailed(
                    AUTH_USER_NOT_LOGGED_IN)

            username = response.json().get('username')
        else:
            cached = True

        try:
            # Returns a username from the user_list
            profile = UserProfile.objects.get(ona_username=username)
        except UserProfile.DoesNotExist:  # pylint: disable=no-member
            raise exceptions.AuthenticationFailed(
                AUTH_USER_DOESNT_EXIST
            )
        else:
            # Cache the key and username for a set amount of time
            # Only if the user is not already cached
            if not cached:
                cache.set(key, username, settings.TEMP_TOKEN_TIMEOUT)

            return (profile.user, None)

    def authenticate_header(self, request):
        return 'TempToken'
