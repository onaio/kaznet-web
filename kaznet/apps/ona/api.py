"""
Module containing methods that communicate
with the OnaData API
"""
from urllib.parse import urljoin

import dateutil.parser
import requests
from requests.adapters import HTTPAdapter
# pylint: disable=import-error
from requests.packages.urllib3.util.retry import Retry

from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.settings.common import ONA_BASE_URL, ONA_PASSWORD, ONA_USERNAME


def request_session(
        url: str,
        method: str,
        payload: dict = None,
        retries=3,
        backoff_factor=1,
        status_forcelist=(500, 502, 504),
):  # pylint: disable=too-many-arguments
    """
    Custom Method that takes in a URL and optionally retries,
    backoff_factor and status_forcelist. It creates a Request
    Session and Retry Object and mounts a HTTP Adapter to the
    Session and Sends a request to the url. It then returns the Response.
    """
    session = requests.Session()
    retries = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    if method == 'GET':
        response = session.get(
            url, auth=(ONA_USERNAME, ONA_PASSWORD), params=payload
            )
        return response
    elif method == 'POST':
        response = session.post(
            url, auth=(ONA_USERNAME, ONA_PASSWORD), data=payload
            )
        return response
    else:
        response = None

    return response


def request(
        url: str,
        args: dict = None,
        method: str = 'GET'
):
    """
    Custom Method that requests data from requests_session
    and confirms it has a valid JSON return
    """
    response = request_session(url, method, args)

    try:
        return response.json()
    except ValueError:
        return None
    except AttributeError:
        return None


def get_projects(username: str = ONA_USERNAME):
    """
    Custom Method that returns all Projects owned
    by the User from the OnaData API
    """
    args = {'owner': username}
    url = urljoin(ONA_BASE_URL, 'api/v1/projects')
    projects_data = request(url, args)

    return projects_data


def process_projects(projects_data: dict):
    """
    Takes a Dictionary containing Data about Projects
    and Processes each one
    """
    if projects_data is not None:
        for project_data in projects_data:
            process_project(project_data)


def process_project(project_data: dict):
    """
    Custom method that takes a projects data and creates
    an Instance of that Project
    """
    projectid = project_data.get('projectid')

    if projectid is not None:
        obj, created = Project.objects.get_or_create(
            ona_pk=projectid,
            defaults={
                'name': project_data.get('name'),
                'deleted_at': project_data.get('deleted_at'),
                'last_updated': project_data.get('date_modified')
                }
            )

        if created is False:
            # If object was not created this means it exists so we check
            # if it needs updating or not.

            # Turns the project_data['date_modified'] into a datetime object
            # for easier comparison
            mocked_date = dateutil.parser.parse(project_data.get(
                'date_modified'))
            if mocked_date is not None:
                if obj.last_updated != mocked_date:
                    obj.name = project_data.get('name')
                    obj.last_updated = project_data.get('date_modified')
                    obj.deleted_at = project_data.get('deleted_at')
                    obj.save()


def process_xforms(forms_data: dict, project_id: int):
    """
    Takes a Dictionary containing Data about Forms
    and process each one
    """
    if forms_data is not None:
        for xform_data in forms_data:
            process_xform(xform_data, project_id)


def process_xform(xform_data: dict, project_id: int):
    """
    Takes a Dictionary containing Data about an XForm
    and Creates or Updates that XForm Instance
    """
    xformid = xform_data.get('formid')

    if xformid is not None:
        obj, created = XForm.objects.get_or_create(
            ona_pk=xformid,
            defaults={
                'title': xform_data.get('name'),
                'id_string': xform_data.get('id_string'),
                'project_id': project_id
            }
            )

        if created is False:
            # If object was not created this means it exists so we check
            # if it needs updating or not.

            # We check using title of form since that is the only changeable
            # field returned in response
            if obj.title != xform_data.get('name'):
                obj.title = xform_data.get('name')
                obj.id_string = xform_data.get('id_string')
                obj.save()


def get_instances(xform: object):
    """
    Takes an XForm Object and Retrieves its Instances from
    OnaData
    """
    xformid = xform.ona_pk
    end_page = None
    start = 0
    instances_data = []

    while end_page is None:
        url = urljoin(ONA_BASE_URL, f'api/v1/data/{xformid}')
        args = {'start': start, 'limit': 100}
        data = request(url, args)
        start = start + 100
        if data == []:
            end_page = True
            break
        elif data is not None:
            instances_data = instances_data + data

    return instances_data


def process_instances(instances_data: dict, xform: object):
    """
    Takes a Dictionary Containing Data on Instances
    and Process them
    """
    if instances_data is not None:
        if instances_data != []:
            for instance_data in instances_data:
                process_instance(instance_data, xform)


def process_instance(instance_data: dict, xform: object):
    """
    Takes a Dictionary Containong Data on an Instance
    and Creates or Updates that Instance
    """
    instanceid = instance_data.get('_id')

    if instanceid is not None:
        obj, created = Instance.objects.get_or_create(
            ona_pk=instanceid,
            defaults={
                'xform': xform,
                'json': instance_data
            }
        )

        if created is False:
            # If object was not created this means it exists so we check
            data = obj.json
            edited = data.get('_edited')
            data_edited = instance_data.get('_edited')
            last_updated = instance_data.get('_last_edited')

            if edited is not True and data_edited is True:
                obj.last_updated = instance_data.get('_last_edited')
                obj.json = instance_data
                obj.save()

            mocked_date = dateutil.parser.parse(last_updated)

            if obj.last_updated != mocked_date:
                obj.json = instance_data
                obj.last_updated = instance_data.get('_last_edited')
                obj.save()
