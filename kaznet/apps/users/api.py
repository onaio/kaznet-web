"""
API Methods For Kaznet User App
"""
from json.decoder import JSONDecodeError
from urllib.parse import urljoin

from kaznet.apps.ona.api import request_session


def create_ona_user(  # pylint: disable=too-many-arguments
        api_root: str,
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
        urljoin(api_root, 'api/v1/profiles'),
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
        created = False
    else:
        created = True

    try:
        data = response.json()
    except JSONDecodeError:
        data = None

    return (created, data)


def add_team_member(
        api_root: str,
        username: str,
        team_id: int
):
    """
    Custom Method that adds a User to the Projects
    Org Members List
    """
    data = None
    response = request_session(
        urljoin(api_root, f'api/v1/teams/{team_id}/members'),
        'POST',
        payload={
            'username': username
        }
    )

    if response.status_code != 201:
        added = False
    else:
        added = True

    try:
        data = response.json()
    except JSONDecodeError:
        data = None

    return (added, data)


def update_details(  # pylint: disable=too-many-arguments
        api_root: str,
        username: str,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        password: str = None
):
    """
    Custom Method that Updates User Details
    """
    data = None

    response = request_session(
        urljoin(api_root, f'api/v1/profiles/{username}'),
        'PATCH',
        payload={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password
        }
    )

    if response.status_code != 200:
        updated = False
    else:
        updated = True

    try:
        data = response.json()
    except JSONDecodeError:
        data = None

    return (updated, data)


def change_password(
        api_root: str,
        username: str,
        old_password: str,
        password: str
):
    """
    Custom Method that Changes Password
    """
    response = request_session(
        urljoin(
            api_root,
            f'api/v1/profiles/{username}/change_password'),
        'POST',
        payload={
            'current_password': old_password,
            'new_password': password
        }
    )

    if response.status_code != 204:
        updated = False
    else:
        updated = True

    return updated
