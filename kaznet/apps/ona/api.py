"""
Module containing methods that communicate
with the OnaData API
"""
from urllib.parse import urljoin

from django.contrib.auth.models import User

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
    Custom Method that takes in a URL, Method(GET / POST) and optionally
    retries, backoff_factor and status_forcelist. It creates a Request
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


def get_project(url: str):
    """
    Custom Method that returns a specific project
    from the OnaData API
    """
    return request(url)


def process_projects(projects_data: dict):
    """
    Custom Method that takes a Dictionary containing
    Data about Projects and Processes each one using
    the process_project method
    """
    if projects_data is not None:
        for project_data in projects_data:
            process_project(project_data)


def process_project(project_data: dict):
    """
    Custom method that takes a projects data and creates or
    Update an Object of a Project
    """
    project_id = project_data.get('projectid')

    if project_id is not None:
        obj, created = Project.objects.get_or_create(
            ona_pk=project_id,
            defaults={
                'name': project_data.get('name'),
                'deleted_at': project_data.get('deleted_at'),
                'last_updated': project_data.get('date_modified')
                }
            )

        if not created:
            # If object was not created this means it exists so we check
            # if it needs updating or not.

            # Turns the project_data['date_modified'] into a datetime object
            # for easier comparison
            last_updated_ona = dateutil.parser.parse(project_data.get(
                'date_modified'))
            if last_updated_ona is not None:
                if obj.last_updated != last_updated_ona:
                    obj.name = project_data.get('name')
                    obj.last_updated = project_data.get('date_modified')
                    obj.deleted_at = project_data.get('deleted_at')
                    obj.save()


def get_xform(xform_id: int):
    """
    Custom Method that return a specific Form
    """
    return request(urljoin(ONA_BASE_URL, f'api/v1/forms/{xform_id}'))


def process_xforms(forms_data: dict, project_id: int):
    """
    Custom Method that takes in a Dictionary containing Data
    of Forms from OnaData API and a Project ID then processes
    each Form by using the process_xform method
    """
    if forms_data is not None:
        for xform_data in forms_data:
            process_xform(xform_data, project_id=project_id)


def process_xform(xform_data: dict, project_id: int = None):
    """
    Custom Method that takes in a Dictionary containing Data
    about an XForm and a Project ID then creates or updates
    an XForm Object
    """
    xform_id = xform_data.get('formid')

    # Confirm that the XForm_data contains the XFormID
    if xform_id is not None:
        if project_id is None:
            url = xform_data.get('project')
            project = get_project_obj(project_url=url)
        else:
            project = get_project_obj(project_id)

        title = xform_data.get('name') or xform_data.get('title')

        obj, created = XForm.objects.get_or_create(
            ona_pk=xform_id,
            defaults={
                'title': title,
                'id_string': xform_data.get('id_string'),
                'project_id': project.id,
                'last_updated': xform_data.get('last_updated_at')
            }
            )

        if not created:

            last_updated_ona = dateutil.parser.parse(xform_data.get(
                'date_modified'))

            if last_updated_ona and obj.last_updated != last_updated_ona:
                obj.last_updated = last_updated_ona
            if obj.title != title:
                obj.title = title

            obj.save()


def get_project_obj(ona_project_id: int = None, project_url: str = None):
    """
    Custom Method that returns a Project object
    """
    if ona_project_id is not None:
        try:
            return Project.objects.get(ona_pk=ona_project_id)
        except Project.DoesNotExist:  # pylint: disable=no-member
            project_data = get_project(
                urljoin(ONA_BASE_URL, f'api/v1/projects/{ona_project_id}'))
            process_project(project_data)
            return Project.objects.get(ona_pk=ona_project_id)
    else:
        project_data = get_project(project_url)
        ona_project_id = project_data.get('projectid')
        process_project(project_data)
        return Project.objects.get(ona_pk=ona_project_id)


def get_instances(xform_id: int):
    """
    Custom Method that Takes in an XForm Object and Retrieves
    and returns Data on its Instances from OnaData
    """
    end_page = None
    start = 0

    while end_page is None:
        url = urljoin(ONA_BASE_URL, f'api/v1/data/{xform_id}')
        args = {'start': start, 'limit': 100}
        data = request(url, args)
        start = start + 100
        if data == []:
            end_page = True
            break
        yield data


def get_instance(xform_id: int, instance_id: int):
    """
    Custom Method that takes in an XFormID and InstanceID
    and retrieves instance date
    """
    return request(
        urljoin(ONA_BASE_URL, f'api/v1/data/{xform_id}/{instance_id}'))


def process_instances(instances_data: iter, xform: object = None):
    """
    Custom Method that takes in a Dictionary containing Data
    of Instances and an XForm object then processes the Instances
    by sending each one to process_instance
    """
    if instances_data is not None:
        for instance_data_list in instances_data:
            for instance_data in instance_data_list:
                process_instance(instance_data, xform)


def process_instance(instance_data: dict, xform: object = None):
    """
    Custom Method that takes in a Dictionary containing Data on
    an Instance and Creates or Updates an Instance Object
    """
    instanceid = instance_data.get('_id')

    if instanceid is not None:
        # Check whether XForm has been Passed
        # If it hasn't try get an XForm Object using xform_id
        if xform is None:
            xform_id = instance_data.get('_xform_id')
            xform = get_xform_obj(xform_id)

        try:
            user = User.objects.get(
                username=instance_data.get("_submitted_by"))
        except User.DoesNotExist:  # pylint: disable=no-member
            pass
        else:
            if xform is not None:
                try:
                    obj = Instance.objects.get(ona_pk=instanceid)
                except Instance.DoesNotExist:  # pylint: disable=no-member
                    # new object
                    obj = Instance(
                        ona_pk=instanceid,
                        xform=xform,
                        user=user,
                        last_updated=instance_data.get('_last_edited'),
                        json=instance_data
                    )
                    obj.save()

                    return obj

                else:
                    # existing object
                    # If object was not created this means
                    # it exists so we check
                    data = obj.json
                    edited = data.get('_edited')
                    data_edited = instance_data.get('_edited')
                    last_updated = instance_data.get('_last_edited')
                    last_updated_ona = dateutil.parser.parse(last_updated)

                    if (edited is not True and data_edited is True) or (
                            obj.last_updated != last_updated_ona
                    ):
                        obj.last_updated = instance_data.get('_last_edited')
                        obj.json = instance_data
                        obj.save()
                    return obj
    return None


def get_xform_obj(ona_xform_id: int):
    """
    Custom Method that takes in an XForms ona pk
    and returns the object
    """
    try:
        xform = XForm.objects.get(ona_pk=ona_xform_id)
        return xform
    except XForm.DoesNotExist:  # pylint: disable=no-member
        xform_data = get_xform(ona_xform_id)
        process_xform(xform_data)
        return XForm.objects.filter(ona_pk=ona_xform_id).first()


def create_or_update_instance_hook(instance_data: dict):
    """
    Custom Method that takes instance data and creates or Updates
    an Instance Then Returns True if Instance was created or updated
    """
    instance_obj = process_instance(instance_data)
    if instance_obj is None:
        return False
    return True
