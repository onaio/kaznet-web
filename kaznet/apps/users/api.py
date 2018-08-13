"""
API Methods For Kaznet User App
"""
from django.conf import settings

from kaznet.apps.ona.api import request_session


def create_ona_user(
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str
):
    """
    Custom Method that creates an Ona User
    and returns Errors That Occur.
    """
    errors = None
    response = request_session(
        settings.ONA_CREATE_USER_URL,
        'POST',
        payload={
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
    )

    if response.status_code != 200:
        errors = response.json()
        created = False
    else:
        created = True

    return (created, errors)
