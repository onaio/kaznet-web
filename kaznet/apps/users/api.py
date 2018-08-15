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

    if response.status_code != 201:
        data = response.json()
        created = False
    else:
        data = response.json()
        created = True

    return (created, data)


def add_team_member(
        username: str
):
    """
    Custom Method that adds a User to the Projects
    Org Members List
    """
    data = None
    response = request_session(
        settings.ONA_ORG_TEAM_MEMBERS_URL,
        'POST',
        payload={
            'username': username
        }
    )

    if response.status_code != 201:
        data = response.json()
        added = False
    else:
        added = True

    return (added, data)
