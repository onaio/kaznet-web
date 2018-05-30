"""
Module containing methods that communicates
with the Onadata API
"""
import dateutil.parser
import requests

from requests.adapters import HTTPAdapter
# pylint: disable=import-error
from requests.packages.urllib3.util.retry import Retry

from kaznet.apps.ona.models import OnaInstance, OnaProject, XForm
from kaznet.settings.common import ONA_BASE_URL, ONA_PASSWORD, ONA_USERNAME


def get_projects(username: str = ONA_USERNAME):
    """
    Custom Method that takes in an Ona Users username and
    Makes a request to onadata api. Takes the response gotten
    and Loops through it while passing Project data contained in response
    to the process_project() method.
    """

    url = f"{ONA_BASE_URL}/projects?owner={username}"
    projects_data = requests_session(url).json()

    for project_data in projects_data:
        process_project(project_data)


def process_project(project_data: dict):
    """
    Custom Method that takes a Dictionary containing Project Data and Creates
    or Updates an OnaProject Object Then It Retrieves the Forms in Project Data
    and Loops through each item while passing it to the process_xform() method.
    """

    obj, created = OnaProject.objects.get_or_create(
        ona_pk=project_data['projectid'],
        defaults={
            'name': project_data['name'],
            'deleted_at': project_data['deleted_at'],
            'ona_last_updated': project_data['date_modified']
            }
        )

    if created is False:
        # If object was not created this means it exists so we check
        # if it needs updating or not.

        # Turns the project_data['date_modified'] into a datetime object
        # for easier comparison
        mocked_date = dateutil.parser.parse(project_data['date_modified'])

        if obj.ona_last_updated != mocked_date:
            obj.name = project_data['name']
            obj.ona_last_updated = project_data['date_modified']
            obj.deleted_at = project_data['deleted_at']
            obj.save()

    for xform_data in project_data['forms']:
        # Creates form
        process_xform(xform_data, obj.ona_pk)


def get_xform(form_id: int, project_obj: object):
    """
    Custom Method that takes in a form id from ona and a OnaProject Object.
    Requests data for the specific formid and creates or updates an XForm
    Object, Then it passes the created/updated obj to get_instances().
    """
    url = f"{ONA_BASE_URL}/forms/{form_id}"
    xform_data = requests_session(url).json()

    obj, created = XForm.objects.get_or_create(
        ona_pk=xform_data['formid'],
        defaults={
            'title': xform_data['title'],
            'id_string': xform_data['id_string'],
            'ona_last_updated': xform_data['last_updated_at'],
            'ona_project_id': project_obj.ona_pk,
            }
        )

    if created is False:
        # If object was not created this means it exists so we check
        # if it needs updating or not.

        mocked_date = dateutil.parser.parse(xform_data['last_updated_at'])
        if obj.ona_last_updated != mocked_date:
            obj.title = xform_data['title']
            obj.id_string = xform_data['id_string']
            obj.ona_last_updated = xform_data['last_updated_at']
            obj.save()

    get_instances(obj)


def process_xform(xform_data: dict, project_obj_pk: int):
    """
    Custom Method thats takes in a Dictionary containing XForm Data
    and a OnaProject Object. Requests data for the specific formid
    and creates or updates an XForm Object, Then it passes the XForm
    object to get_instances().
    """
    obj, created = XForm.objects.get_or_create(
        ona_pk=xform_data['formid'],
        defaults={
            'title': xform_data['name'],
            'id_string': xform_data['id_string'],
            'ona_project_id': project_obj_pk
            }
        )

    if created is False:
        # If object was not created this means it exists so we check
        # if it needs updating or not.

        # We check using title of form since that is the only changeable
        # field returned in response
        if obj.title != xform_data['name']:
            obj.title = xform_data['name']
            obj.id_string = xform_data['id_string']
            obj.save()

    get_instances(obj)


def get_instances(xform: object):
    """
    Custom Method that takes in an XForm Object and Retrieves
    Its Instances/Data from the OnaData Api. Then, it loops
    through the received Instances/Data and passes each individual
    Instance/Data to process_instance()
    """
    xformid = xform.ona_pk
    end_page = None
    start = 0

    while end_page is None:
        url = f"{ONA_BASE_URL}/data/{xformid}?start={start}&limit=100"
        instances_data = requests_session(url).json()

        if instances_data == []:
            end_page = True
            break

        for instance_data in instances_data:
            process_instance(instance_data, xform)

        start = start + 100


def process_instance(instance_data: dict, xform: object):
    """
    Custome Method that takes in a Dictionary containing Instances
    Data and an XForm Object. It Creates or Updates an OnaInstance
    Object using the inputs.
    """
    obj, created = OnaInstance.objects.get_or_create(
        ona_pk=instance_data['_id'],
        defaults={
            'xform': xform,
            'json': instance_data
            }
        )

    if created is False:
        # If object was not created this means it exists so we check
        # if it needs updating or not.
        if instance_data['_edited'] is True:
            if obj.edited is not True:
                obj.ona_last_updated = instance_data['_last_edited']
                obj.edited = True

            mocked_date = dateutil.parser.parse(instance_data['_last_edited'])
            if obj.ona_last_updated != mocked_date:
                obj.json = instance_data
                obj.ona_last_updated = instance_data['_last_edited']
                obj.save()


def requests_session(
        url: str,
        retries=3,
        backoff_factor=1,
        status_forcelist=(500, 502, 504),
):
    """
    Custom Method that takes in a URL and optionally retries,
    backoff_factor and status_forcelist. It creates a Request
    Session and Retry Object and mounts a HTTP Adapter to the
    Session and Sends a request to the url. It then returns the Response.
    """

    session = requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https', adapter)
    response = session.get(url, auth=(ONA_USERNAME, ONA_PASSWORD))

    return response
