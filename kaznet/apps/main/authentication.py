"""
Custom Authentication Module
"""
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext as _

from rest_framework import exceptions
from rest_framework.authentication import (TokenAuthentication,
                                           get_authorization_header)

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
            message = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(message)
        elif len(auth) > 2:
            message = _('Invalid token header. '
                        'Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(message)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        validation_endpoint = urljoin(
            settings.ONA_BASE_URL, 'api/v1/user')
        user_list = []
        cached_user = cache.get(key)

        # We add the cached_user result to "user_list" list
        user_list.append(cached_user)

        if cached_user is None:
            response = request_session(
                validation_endpoint,
                'GET',
                headers={'Authorization': f'TempToken ${key}'}
                )

            if response.status_code != 200:
                raise exceptions.AuthenticationFailed(
                    _('User not logged into Ona.'))

            request_user = response.json().get('username')
            user_list.append(request_user)

        try:
            # Returns a username from the user_list
            user = next(name for name in user_list if name is not None)
            profile = UserProfile.objects.get(ona_username=user)

            # Cache the key and username for a set amount of time
            if cached_user is None:
                cache.set(key, request_user, settings.TEMP_TOKEN_TIMEOUT)

            return (profile, None)
        except UserProfile.DoesNotExist:  # pylint: disable=no-member
            raise exceptions.AuthenticationFailed(
                _('Invalid User.')
            )

    def authenticate_header(self, request):
        return 'TempToken'
