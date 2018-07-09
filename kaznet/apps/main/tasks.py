"""
Celery tasks module for main Kaznet app
# """
from celery import task

from kaznet.apps.main.models import Task
from kaznet.apps.main.utils import create_occurrences


@task(name="task_create_occurrences")
def task_create_occurrences(task_id):
    """
    Celery task that calls create_occurrences for a task
    """
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:  # pylint: disable=no-member
        pass
    else:
        create_occurrences(task)
