"""
Celery tasks module for Ona app
"""
from datetime import timedelta
from time import sleep
from urllib.parse import urljoin

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils import timezone

from celery import task as celery_task

from kaznet.apps.main.models import Task
from kaznet.apps.ona.api import (create_filtered_data_sets,
                                 create_form_webhook, fetch_missing_instances,
                                 get_and_process_xforms, get_projects,
                                 process_projects, sync_deleted_instances,
                                 sync_updated_instances,
                                 update_user_profile_metadata)
from kaznet.apps.ona.models import XForm


@celery_task(name="task_fetch_projects")  # pylint: disable=not-callable
def task_fetch_projects(username: str):
    """
    Fetches and processes projects from Onadata
    """
    # get the projects from Onadata's API
    projects = get_projects(username=username)
    # save the projects locally
    process_projects(projects)
    # go through each project and process its forms
    for project in projects:
        project_forms = project.get('forms')
        project_id = project.get('projectid')
        if project_forms and project_id:
            task_process_project_xforms.delay(
                forms=project_forms, project_id=int(project_id))
            sleep(0.1)  # to avoid overload on onadata API


# pylint: disable=not-callable
@celery_task(name="task_process_project_xforms")
def task_process_project_xforms(forms: list, project_id: int):
    """
    Simple processes XForms contained in the project response
    from Onadata
    """
    get_and_process_xforms(forms_data=forms, project_id=project_id)


# pylint: disable=not-callable
@celery_task(name="task_fetch_form_missing_instances")
def task_fetch_form_missing_instances(xform_id: int):
    """
    Gets and processes instances from Onadata's API
    """
    try:
        xform = XForm.objects.get(id=xform_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        fetch_missing_instances(form_id=xform.ona_pk)


# pylint: disable=not-callable
@celery_task(name="task_sync_form_updated_instances")
def task_sync_form_updated_instances(xform_id: int):
    """
    Checks for updated instances for a form and then updates them
    """
    try:
        xform = XForm.objects.get(id=xform_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        sync_updated_instances(form_id=xform.ona_pk)


# pylint: disable=not-callable
@celery_task(name="task_sync_updated_instances")
def task_sync_updated_instances():
    """
    Checks for updated instances for all forms and then updates them
    """
    xforms = XForm.objects.filter(deleted_at=None)
    for xform in xforms:
        if xform.has_task:
            task = xform.task
            if task is not None and task.status == Task.ACTIVE:
                task_sync_form_updated_instances.delay(xform_id=xform.id)


# pylint: disable=not-callable
@celery_task(name="task_fetch_missing_instances")
def task_fetch_missing_instances():
    """
    Gets and processes instances for all known XForms
    """
    forms = XForm.objects.filter(deleted_at=None)
    for form in forms:
        if form.has_task:
            the_task = form.task
            if the_task is not None and the_task.status == Task.ACTIVE:
                task_fetch_form_missing_instances.delay(xform_id=form.id)


@celery_task(name="task_process_user_profiles")  # pylint: disable=not-callable
def task_process_user_profiles():
    """
    Process the User Model Objects and Updates All Objects that need
    Updating
    """
    time = timezone.now() - timedelta(minutes=30)
    user_list = User.objects.filter(last_login__gt=time)

    for user in user_list:
        task_update_user_profile.delay(
            ona_username=user.userprofile.ona_username)


@celery_task(name="task_update_user_profile")  # pylint: disable=not-callable
def task_update_user_profile(ona_username: str):
    """
    Updates Userprofile metadata
    """
    update_user_profile_metadata(ona_username)


# pylint: disable=not-callable
@celery_task(name="task_auto_create_filtered_data_sets")
def task_auto_create_filtered_data_sets(
        form_id: int, project_id: int, form_title: str):
    """
    Takes ona form filtered data sets
    """
    create_filtered_data_sets(
        form_id=form_id, project_id=project_id, form_title=form_title)


@celery_task(name="task_task_create_form_webhook")
def task_create_form_webhook(form_id: int):
    """
    Creates an Onadata webhook for the form
    """
    current_site = Site.objects.get_current()
    service_url = urljoin(current_site.domain, reverse('webhook'))
    create_form_webhook(
        form_id=form_id,
        service_url=service_url
    )


# pylint: disable=not-callable
@celery_task(name="task_sync_form_deleted_instances")
def task_sync_form_deleted_instances(xform_id: int):
    """
    Checks for deleted instances for a form and then syncs them
    """
    try:
        the_xform = XForm.objects.get(id=xform_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        sync_deleted_instances(form_id=the_xform.ona_pk)


# pylint: disable=not-callable
@celery_task(name="task_sync_deleted_instances")
def task_sync_deleted_instances():
    """
    Checks for deleted instances for all forms and then syncs them
    """
    xforms = XForm.objects.filter(deleted_at=None)
    for xform in xforms:
        task_sync_form_deleted_instances.delay(xform_id=xform.id)
