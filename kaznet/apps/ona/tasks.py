"""
Celery tasks module for Ona app
"""
from time import sleep
from celery import task as celery_task

from kaznet.apps.main.models import Task
from kaznet.apps.ona.api import (get_instances, get_projects, process_instance,
                                 process_projects, process_xforms)
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
            task_fetch_project_xforms.delay(
                forms=project_forms, project_id=int(project_id))
            sleep(0.1)  # to avoid overload on onadata API


@celery_task(name="task_fetch_project_xforms")  # pylint: disable=not-callable
def task_fetch_project_xforms(forms: list, project_id: int):
    """
    Fetches and processes XForms from Onadata
    """
    process_xforms(forms_data=forms, project_id=project_id)


@celery_task(name="task_fetch_form_instances")  # pylint: disable=not-callable
def task_fetch_form_instances(xform_id: int):
    """
    Gets and processes instances from Onadata's API
    """
    try:
        xform = XForm.objects.get(id=xform_id)
    except XForm.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        instances_iter = get_instances(xform_id=xform.ona_pk)
        for _ in instances_iter:
            instance_data_list = _
            for instance_data in instance_data_list:
                process_instance(instance_data=instance_data, xform=xform)


@celery_task(name="task_fetch_all_instances")  # pylint: disable=not-callable
def task_fetch_all_instances():
    """
    Gets and processes instances for all known XForms
    """
    forms = XForm.objects.filter(deleted_at=None)
    for form in forms:
        if form.has_task:
            the_task = form.task.first()
            if the_task is not None and the_task.status == Task.ACTIVE:
                task_fetch_form_instances.delay(xform_id=form.id)
