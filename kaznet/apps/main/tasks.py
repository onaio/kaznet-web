"""
Celery tasks module for main Kaznet app
"""
from celery import task as celery_task

from kaznet.apps.main.api import create_submission
from kaznet.apps.main.models import Task
from kaznet.apps.main.utils import create_occurrences
from kaznet.apps.ona.models import Instance


@celery_task(name="task_create_occurrences")  # pylint: disable=not-callable
def task_create_occurrences(task_id: int):
    """
    Celery task that calls create_occurrences for a task
    """
    try:
        task_instance = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        create_occurrences(task_instance)


@celery_task(name="task_create_submission")  # pylint: disable=not-callable
def task_create_submission(instance_id: int):
    """
    Takes an Instance and validates it and creates a Submission
    """
    try:
        instance = Instance.objects.get(pk=instance_id)
    except Instance.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        create_submission(ona_instance=instance)
