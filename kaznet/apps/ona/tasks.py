"""
Celery tasks module for Ona app
"""
from celery import task as celery_task

from kaznet.apps.ona.api import get_projects, process_projects, process_xforms


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


@celery_task(name="task_fetch_project_xforms")  # pylint: disable=not-callable
def task_fetch_project_xforms(forms: list, project_id: int):
    """
    Fetches and processes XForms from Onadata
    """
    process_xforms(forms_data=forms, project_id=project_id)
