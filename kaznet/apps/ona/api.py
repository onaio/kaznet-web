"""
Module containing methods that communicate
with the OnaData API
"""
import json
from urllib.parse import urljoin

import dateutil.parser
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from requests.adapters import HTTPAdapter
# pylint: disable=import-error
from requests.packages.urllib3.util.retry import Retry

from kaznet.apps.main.common_tags import (FILTERED_DATASETS_FIELD_NAME,
                                          HAS_FILTERED_DATASETS_FIELD_NAME,
                                          HAS_WEBHOOK_FIELD_NAME,
                                          KAZNET_WEBHOOK_NAME,
                                          WEBHOOK_FIELD_NAME)
from kaznet.apps.main.models import Submission
from kaznet.apps.ona.models import Instance, Project, XForm
from kaznet.apps.ona.utils import (check_if_users_can_submit_to_form,
                                   delete_instance, delete_project,
                                   delete_xform)
from kaznet.apps.users.models import UserProfile

SUCCESS_STATUSES = [200, 201]


def request_session(
        url: str,
        method: str,
        payload: dict = None,
        headers: dict = None,
        username: str = settings.ONA_USERNAME,
        password: str = settings.ONA_PASSWORD,
        retries=3,
        backoff_factor=1.1,
        status_forcelist=(500, 502, 504),
):  # pylint: disable=too-many-arguments
    """
    Custom Method that takes in a URL, Method(GET / POST) and optionally
    retries, backoff_factor and status_forcelist. It creates a Request
    Session and Retry Object and mounts a HTTP Adapter to the
    Session and Sends a request to the url. It then returns the Response.

    The backoff policy is documented here:
    https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    """  # noqa
    session = requests.Session()
    retries = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist)

    if username is not None:
        basic_auth = (username, password)
    else:
        basic_auth = None

    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    if method == 'GET':
        response = session.get(
            url, auth=basic_auth, params=payload, headers=headers)
        return response
    if method == 'POST':
        response = session.post(
            url, auth=basic_auth, json=payload, headers=headers)
        return response
    if method == 'PATCH':
        response = session.patch(
            url, auth=basic_auth, json=payload, headers=headers)
        return response
    if method == 'PUT':
        response = session.put(
            url, auth=basic_auth, json=payload, headers=headers)
        return response
    if method == 'DELETE':
        response = session.delete(url, auth=basic_auth, headers=headers)
        return response

    return None


def convert_ona_to_kaznet_submission_status(ona_status: str):
    """
    Convert Ona Instance statuses (1, 2, 3) to kaznet submission statuses
    ('a', 'b', 'c')
    """
    if ona_status == settings.ONA_SUBMISSION_REVIEW_APPROVED:
        return Submission.APPROVED
    if ona_status == settings.ONA_SUBMISSION_REVIEW_REJECTED:
        return Submission.REJECTED
    if ona_status == settings.ONA_SUBMISSION_REVIEW_PENDING:
        return Submission.PENDING
    return None


def convert_kaznet_to_ona_submission_status(kaznet_status: str):
    """
    Convert kaznet submission statuses ('a', 'b', 'c') to Ona Instance
    statuses (1, 2, 3)
    """
    if kaznet_status == Submission.APPROVED:
        return settings.ONA_SUBMISSION_REVIEW_APPROVED
    if kaznet_status == Submission.REJECTED:
        return settings.ONA_SUBMISSION_REVIEW_REJECTED
    if kaznet_status == Submission.PENDING:
        return settings.ONA_SUBMISSION_REVIEW_PENDING
    return None


def request(url: str, args: dict = None, method: str = 'GET', headers=None):
    """
    Custom Method that requests data from requests_session
    and confirms it has a valid JSON return
    """
    response = request_session(url, method, args, headers)
    try:
        # you only come here if we can understand the API response
        return response.json()
    except ValueError:
        return None
    except AttributeError:
        return None


def get_projects(username: str = settings.ONA_USERNAME):
    """
    Custom Method that returns all Projects owned
    by the User from the OnaData API
    """
    args = {'owner': username}
    url = urljoin(settings.ONA_BASE_URL, 'api/v1/projects')
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
        Project.objects.update_or_create(
            ona_pk=project_id,
            defaults={
                'name': project_data.get('name'),
                'deleted_at': project_data.get('deleted_at'),
                'last_updated': project_data.get('date_modified'),
                'json': project_data,
            })


def get_xform(xform_id: int):
    """
    Custom Method that return a specific Form
    """
    return request(urljoin(settings.ONA_BASE_URL, f'api/v1/forms/{xform_id}'))


def process_xforms(forms_data: list, project_id: int):
    """
    Custom Method that takes in a list containing Data
    of Forms from OnaData API and a Project ID then processes
    each Form by using the process_xform method
    """
    if forms_data and forms_data is not None:
        for xform_data in forms_data:
            process_xform(xform_data, project_id=project_id)


def get_and_process_xforms(forms_data: list, project_id: int = None):
    """
    Takes a list of XForm dicts and calls get_xform then processes it
    """
    if forms_data and forms_data is not None:
        for xform_data in forms_data:
            ona_xform_id = xform_data.get('formid')
            if ona_xform_id:
                full_xform_data = get_xform(ona_xform_id)
                process_xform(full_xform_data, project_id)


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
        version = xform_data.get('version')

        owner_url = xform_data.get('owner')
        owner = None
        if owner_url is not None:
            owner = owner_url.rsplit("/", 1)[-1]

        json_data = dict(
            owner=owner,
            owner_url=owner_url,
            downloadable=xform_data.get("downloadable", False)
        )

        xform, _ = XForm.objects.update_or_create(
            ona_pk=xform_id,
            defaults={
                'title': title,
                'id_string': xform_data.get('id_string'),
                'version': version,
                'ona_project_id': project.ona_pk,
                'last_updated': xform_data.get('last_updated_at'),
                'json': json_data
            })

        # check if configured correctly
        check_if_users_can_submit_to_form(xform=xform)


def get_project_obj(ona_project_id: int = None, project_url: str = None):
    """
    Custom Method that returns a Project object
    """
    if ona_project_id is not None:
        try:
            return Project.objects.get(ona_pk=ona_project_id)
        except Project.DoesNotExist:  # pylint: disable=no-member
            project_data = get_project(
                urljoin(settings.ONA_BASE_URL,
                        f'api/v1/projects/{ona_project_id}'))
            process_project(project_data)
            return Project.objects.get(ona_pk=ona_project_id)
    else:
        project_data = get_project(project_url)
        ona_project_id = project_data.get('projectid')
        process_project(project_data)
        return Project.objects.get(ona_pk=ona_project_id)


def fetch_form_data(  # pylint: disable=too-many-arguments
    formid: int,  # pylint: disable=bad-continuation
    latest: int = None,  # pylint: disable=bad-continuation
    dataid: int = None,  # pylint: disable=bad-continuation
    dataids_only: bool = False,  # pylint: disable=bad-continuation
    edited_only: bool = False,  # pylint: disable=bad-continuation
    query: dict = None,  # pylint: disable=bad-continuation
):
    """Fetch submission data from Ona API data endpoint.

    Keyword arguments:
    latest -- fetch only recent records.
    dataid -- fetch a record with the matching dataid
    dataids_only -- fetch only record ids.
    edited_only -- fetch only the records that have been edited
    query -- apply a specific query when fetching records.

    Originally copied from: https://github.com/onaio/mspray
    """
    query_params = None
    if latest:
        query_params = {"query": '{"_id":{"$gte":%s}}' % (latest)}
    if dataids_only:
        query_params = {} if query_params is None else query_params
        query_params["fields"] = '["_id"]'
    if edited_only:
        query_params = {"query": '{"_edited":"true"}'}

    if query:
        if query_params and "query" in query_params:
            _query = json.loads(query_params["query"])
            if isinstance(_query, dict):
                _query.update(query)
                query_params["query"] = json.dumps(_query)
        else:
            query_params = {"query": json.dumps(query)}

    if dataid is not None:
        url = urljoin(
            settings.ONA_BASE_URL, f"/api/v1/data/{formid}/{dataid}.json")
    else:
        url = urljoin(settings.ONA_BASE_URL, f"/api/v1/data/{formid}.json")

    return request(url=url, method='GET', args=query_params)


def sync_submission_review(instance_id, ona_review_status):
    """
    ensure Submission is in sync with Submission in onadata.
    """
    args = {"status": ona_review_status,
            "instance": instance_id}
    headers = {"Authorization": "TempToken "+temp_tocken}
    instance = Instance.objects.all().filter(id=instance_id)
    if not instance.json.get("synced_with_ona_data"):
        url = urljoin(settings.ONA_BASE_URL, 'api/v1/submissionreview.json')
        request(url, args, method='POST', headers=headers)


def sync_updated_instances(form_id: int):
    """
    Attempts to get and sync updated instances from Onadata
    """
    try:
        the_xform = XForm.objects.get(ona_pk=form_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        raw_ids = fetch_form_data(
            formid=the_xform.ona_pk,
            dataids_only=True,
            edited_only=True)
        if isinstance(raw_ids, list) and raw_ids:
            pks = [rec['_id'] for rec in raw_ids]
            # next, we fetch data for these ids
            process_instance_ids(list_of_ids=pks, xform=the_xform)


def sync_deleted_instances(form_id: int):
    """
    Attempts to get and sync deleted instances from Onadata
    """
    try:
        the_xform = XForm.objects.get(ona_pk=form_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        raw_ids = fetch_form_data(
            formid=the_xform.ona_pk,
            dataids_only=True)
        if isinstance(raw_ids, list) and raw_ids:
            onadata_instance_pks = [rec['_id'] for rec in raw_ids]
            local_instances = Instance.objects.filter(xform=the_xform)
            deleted_instances = local_instances.exclude(
                ona_pk__in=onadata_instance_pks)
            # delete safely
            for instance in deleted_instances:
                delete_instance(instance)


def fetch_missing_instances(form_id: int):
    """
    Attempts to fetch missing instances from Onadata
    """
    try:
        xform = XForm.objects.get(ona_pk=form_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        # does this form even have submissions?
        raw_id_data = fetch_form_data(formid=form_id, dataids_only=True)
        if isinstance(raw_id_data, list) and raw_id_data:
            # we have some submissions, lets get the submissions ids from Ona
            all_ids = [rec['_id'] for rec in raw_id_data]
            all_ids.sort()

            # lets get existing ids
            existing_ids = Instance.objects.filter(
                xform__ona_pk=form_id).values_list('ona_pk', flat=True)

            # now we get the missing ids
            missing_ids = sorted(list(set(all_ids) - set(existing_ids)))

            # next, we fetch data for these ids
            process_instance_ids(list_of_ids=missing_ids, xform=xform)


def process_instance_ids(list_of_ids: list, xform: object):
    """
    Takes a list of Onadata Instance ids and processes them
    """
    for dataid in list_of_ids:
        record = fetch_form_data(formid=xform.ona_pk, dataid=dataid)
        if record and isinstance(record, dict):
            # save it locally
            process_instance(
                instance_data=record, xform=xform)


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
            # the user who collected this data does not exist locally
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
                        json=instance_data)
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

                    last_updated_ona = None
                    if last_updated is not None:
                        last_updated_ona = dateutil.parser.parse(last_updated)

                    if (edited is not True and data_edited is True) or (
                            obj.last_updated != last_updated_ona):
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
    except XForm.DoesNotExist:  # pylint: disable=no-member
        xform_data = get_xform(ona_xform_id)
        process_xform(xform_data)
        return XForm.objects.filter(ona_pk=ona_xform_id).first()
    else:
        return xform


def process_ona_webhook(instance_data: dict):
    """
    Custom Method that takes instance data and creates or Updates
    an Instance Then Returns True if Instance was created or updated
    """
    instance_obj = process_instance(instance_data)
    if instance_obj is None:
        return False
    return True


def get_ona_profile_data(key: str, username: str):
    """
    Custom method that fetches the user's profile data
    using a TempToken from OnaData API
    """
    data = None
    headers = {'Authorization': f'TempToken {key}'}
    response = request_session(
        urljoin(settings.ONA_BASE_URL, f'api/v1/profiles/{username}/'),
        'GET',
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()

    return data


def update_user_profile_metadata(ona_username: str, token_key: str = None):
    """
    Custom method that updates the user's profile with that at OnaData
    """
    profile = None

    # Try to retrieve the profile associated to the ona_username
    try:
        profile = UserProfile.objects.get(ona_username=ona_username)
    except UserProfile.DoesNotExist:  # pylint: disable=no-member
        pass

    # If profile exists we retrieve token key associated to the user
    # and get their profile data from ONA
    if profile:
        if token_key is None:
            token_key = cache.get(ona_username)

        if token_key is not None:
            ona_profile_data = get_ona_profile_data(
                key=token_key, username=ona_username)

            # If ONA returns data we update out profile Object
            if ona_profile_data is not None:
                ona_metadata = ona_profile_data.get('metadata')
                profile.metadata['last_password_edit'] = ona_metadata.get(
                    'last_password_edit')
                profile.metadata['gravatar'] = ona_profile_data.get('gravatar')

                profile.save()


def create_filtered_dataset(form_id: int, payload: dict):
    """
    Calls the Ona API to create a filtered dataset for a form
    """
    try:
        XForm.objects.get(ona_pk=form_id)  # check if valid form
    except XForm.DoesNotExist:  # pylint: disable=no-member
        return None
    else:
        dataviews_url = urljoin(settings.ONA_BASE_URL, 'api/v1/dataviews')

        response = request_session(
            url=dataviews_url, method='POST', payload=payload)

        return response


def delete_filtered_dataset(form_id: int, dataset_url: int):
    """
    Calls the Ona API to delete a filtered dataset for a form
    """
    try:
        XForm.objects.get(ona_pk=form_id)  # make sure form exists
    except XForm.DoesNotExist:  # pylint: disable=no-member
        return None
    else:
        response = request_session(url=dataset_url, method='DELETE')

        return response


# pylint: disable=too-many-locals
def create_filtered_data_sets(
        form_id: int, project_id: int, form_title: str):
    """
    Custom method that creates filtered data sets for all the
    submission statuses : Approved, Rejected, Pending
    """
    try:
        form = XForm.objects.get(ona_pk=form_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        return None
    else:
        ona_form_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/forms/{form_id}')
        ona_project_url = urljoin(
            settings.ONA_BASE_URL, f'api/v1/projects/{project_id}')

        columns = ['_review_status', '_review_comment', 'instanceID',
                   '_last_edited', '_submitted_by', '_media_all_received']

        # get all fields/columns of form required in creating filtered data set
        form_data = request_session(
            url=urljoin(
                settings.ONA_BASE_URL, f'api/v1/forms/{form_id}/form.json'),
            method='GET'
        )
        if form_data.status_code == 200:
            form_columns = [field['name']
                            for field in form_data.json()['children']]
            columns += form_columns

        payload = {
            'xform': ona_form_url,
            'project': ona_project_url,
            'columns': columns
        }

        done = False
        dataview_responses = []

        for status, status_name in Submission.STATUS_CHOICES:
            ona_status = convert_kaznet_to_ona_submission_status(
                kaznet_status=status)
            if ona_status:
                payload['name'] = f'{form_title} - {status_name}'
                payload['query'] = [
                    {
                        'column': '_review_status',
                        'filter': '=',
                        'value': ona_status,
                        'condition': 'or'
                    }
                ]

                response = create_filtered_dataset(
                    form_id=form_id, payload=payload)

                if response.status_code in SUCCESS_STATUSES:
                    dataview_responses.append(response.json())

        # the entire process is only successful when all the datasets were
        # created successfully
        done = len([
            Submission.APPROVED,
            Submission.REJECTED,
            Submission.PENDING
        ]) == len(dataview_responses)

        if not done:
            # we go ahead and delete the datasets that were created
            for counter, dataview_response in enumerate(dataview_responses):
                del_response = delete_filtered_dataset(
                    form_id=form_id, dataset_url=dataview_response['url'])
                if del_response.status_code == 204:
                    # remove any successfully deleted datasets
                    dataview_responses.pop(counter)

        # save the response that we received from Ona in the form metadata
        # this might be empty in case all datasets were either not successfully
        # created or were all deleted
        if not form.json.get(FILTERED_DATASETS_FIELD_NAME):
            form.json[FILTERED_DATASETS_FIELD_NAME] = []
        form.json[FILTERED_DATASETS_FIELD_NAME] += dataview_responses

        # keep track of whether this form has had datasets successfully created
        form.json[HAS_FILTERED_DATASETS_FIELD_NAME] = done

        form.save()

        return form


def create_form_webhook(
        form_id: int, service_url: str, name: str = KAZNET_WEBHOOK_NAME):
    """
    Creates a rest service webhook via the Onadata API
    """
    try:
        form = XForm.objects.get(ona_pk=form_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        return None
    else:
        # we force name to be str in case KAZNET_WEBHOOK_NAME was a lazily
        # translated object, which will fail when being converted to JSON
        name = str(name)

        restservice_url = urljoin(settings.ONA_BASE_URL, 'api/v1/restservices')
        payload = {
            'xform': form_id,
            'service_url': service_url,
            'name': name
        }
        response = request_session(
            url=restservice_url, method='POST', payload=payload)

        form.json[HAS_WEBHOOK_FIELD_NAME] = response.status_code in [200, 201]
        if not form.json.get(WEBHOOK_FIELD_NAME):
            form.json[WEBHOOK_FIELD_NAME] = []
        form.json[WEBHOOK_FIELD_NAME].append(response.json())
        form.save()

        return response


def sync_deleted_projects(usernames: list):
    """
    Checks for deleted projects on Onadata
    If it finds any, it deletes them locally
    """
    onadata_project_pks = []
    for username in usernames:
        onadata_projects = get_projects(username=username)
        if isinstance(onadata_projects, list) and onadata_projects:
            onadata_project_pks = onadata_project_pks + [
                rec['projectid'] for rec in onadata_projects]

    local_projects = Project.objects.filter(deleted_at=None)
    deleted_projects = local_projects.exclude(ona_pk__in=onadata_project_pks)

    # delete projects safely
    for proj in deleted_projects:
        delete_project(proj)


def sync_deleted_xforms(username: str = settings.ONA_USERNAME):
    """
    Checks for deleted xforms on Onadata
    If it finds any, it deletes them locally
    """
    onadata_projects = get_projects(username=username)
    onadata_projects_pks = [rec['projectid'] for rec in onadata_projects]
    onadata_xform_ids = []
    if isinstance(onadata_projects, list) and onadata_projects:
        for project in onadata_projects:
            project_forms = project.get('forms')
            xform_ids = [x['formid'] for x in project_forms if x.get('formid')]
            onadata_xform_ids = onadata_xform_ids + xform_ids

    local_xforms = XForm.objects.filter(deleted_at=None).filter(
        ona_project_id__in=onadata_projects_pks)

    deleted_xforms = local_xforms.exclude(ona_pk__in=onadata_xform_ids)

    # delete xforms safely
    for xform in deleted_xforms:
        delete_xform(xform)
