"""
Module containing methods that communicates
with the Onadata API
"""
import dateutil.parser
import requests

from kaznet.apps.ona.models import OnaInstance, OnaProject, XForm
from kaznet.settings.common import ONA_BASE_URL, ONA_PASSWORD, ONA_USERNAME


def get_projects(username: str = ONA_USERNAME):
    """
    Makes a request to onadata api and returns the response
    data in json format
    """

    url = f"{ONA_BASE_URL}/projects?owner={username}"
    response = requests.get(url, auth=(ONA_USERNAME, ONA_PASSWORD))
    projects_data = response.json()

    for project_data in projects_data:
        process_project(project_data)


def process_project(projects_data: dict):
    """
    Takes a dict containing project data from Ona and creates
    or updates a project
    """

    obj, created = OnaProject.objects.get_or_create(
        ona_pk=projects_data['projectid'],
        defaults={
            'name': projects_data['name'],
            'created': projects_data['date_created'],
            'modified': projects_data['date_modified'],
            'deleted_at': projects_data['deleted_at'],
            'ona_last_updated': projects_data['date_modified']
            }
        )

    if created is False:
        # If object was not created this means it exists so we check
        # if it needs updating or not.

        # Turns the projects_data['date_modified'] into a datetime object
        # for easier comparison
        mocked_date = dateutil.parser.parse(projects_data['date_modified'])

        if obj.ona_last_updated != mocked_date:
            obj.name = projects_data['name']
            obj.deleted_at = projects_data['deleted_at']
            obj.ona_last_updated = projects_data['date_modified']
            obj.save()

    for xform_data in projects_data['forms']:
        # Creates form
        process_xform(xform_data, obj)


def process_xform(xform_data: dict, obj: object):
    """
    Takes form data and an object and uses it to create
    a Form Instance in the db
    """
    obj, created = XForm.objects.get_or_create(
        ona_pk=xform_data['formid'],
        defaults={
            'title': xform_data['name'],
            'id_string': xform_data['id_string'],
            'ona_project_id': obj.ona_pk
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
    Takes a forms ona id and looks it up on the onadata api
    and creates or updates instances of that form
    """
    xformid = xform.ona_pk
    end_page = None
    start = 0

    while end_page is None:
        url = f"{ONA_BASE_URL}/data/{xformid}?start={start}&limit=100"
        response = requests.get(url, auth=(ONA_USERNAME, ONA_PASSWORD))

        instances_data = response.json()

        if instances_data == []:
            end_page = True
            break

        for instance_data in instances_data:
            process_instance(instance_data, xform)

        start = start + 100


def process_instance(instance_data: dict, xform: object):
    """
    Takes a dict containing the information of an instance
    and creates the instance
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
