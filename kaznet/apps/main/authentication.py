"""
Custom Authentication Module
"""
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.core.cache import cache

from rest_framework import exceptions
from rest_framework.authentication import (TokenAuthentication,
                                           get_authorization_header)

from kaznet.apps.main.common_tags import (AUTH_USER_DOESNT_EXIST,
                                          INVALID_TOKEN_CREDENTIALS_MISSING,
                                          INVALID_TOKEN_SPACES_CONTAINED)
from kaznet.apps.ona.api import request_session
from kaznet.apps.users.models import UserProfile


class OnaTempTokenAuthentication(TokenAuthentication):
    """
    Custom Authentication that authenticates a User Using the OnaData
    User Endpoint
    """

    def authenticate(self, request: object):
        auth = get_authorization_header(request).split()

        # We test for b'temptoken' since get_authorization_header
        # returns the auth in byte
        if not auth or auth[0].lower() != b'temptoken':
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                INVALID_TOKEN_CREDENTIALS_MISSING)
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(
                INVALID_TOKEN_SPACES_CONTAINED)

        return self.authenticate_credentials(auth[1], request)

    # pylint: disable=arguments-differ
    def authenticate_credentials(self, key: str, request: object = None):
        username = cache.get(key)
        cached = False

        if username is None:
            try:
                # Request is usually encoded in utf-8
                auth_key = key.decode('utf-8')
            except AttributeError:
                auth_key = key

            response = request_session(
                settings.ONA_CROSS_AUTHENTICATION_URL,
                'GET',
                username=None,
                password=None,
                headers={'Authorization': f'TempToken {auth_key}'})

            if response.status_code != 200:
                error = response.json()
                raise exceptions.AuthenticationFailed(error['detail'])

            username = response.json().get('username')
        else:
            cached = True

        try:
            # Returns a username from the user_list
            profile = UserProfile.objects.get(ona_username=username)
        except UserProfile.DoesNotExist:  # pylint: disable=no-member
            raise exceptions.AuthenticationFailed(AUTH_USER_DOESNT_EXIST)
        else:
            # Cache the key and username for a set amount of time
            # Only if the user is not already cached
            if not cached:
                # We cache twice. Creating one cache with a Key that is
                # the token key in order to use it for future validation
                # We cache it with the username as the password too, In order
                # to be able to retrieve the key within updation functions
                cache.set(key, username, settings.TEMP_TOKEN_TIMEOUT)
                cache.set(username, key, settings.TEMP_TOKEN_TIMEOUT)
                # send the logged in signal
                if request is not None:
                    user_logged_in.send(
                        sender=profile.user.__class__,
                        request=request,
                        user=profile.user)

            return (profile.user, None)

    def authenticate_header(self, request):
        return 'TempToken'
