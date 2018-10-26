"""
Celery tasks module for main Kaznet app
"""
from datetime import date
from django.utils import timezone
from celery import task as celery_task

from kaznet.apps.main.api import create_submission
from kaznet.apps.main.models import Task
from kaznet.apps.main.models import TaskOccurrence
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


@celery_task(name="task_past_end_date")  # pylint: disable=not-callable
def task_past_end_date():
    """
    Sets Task to expired if end date is in the past or today
    """
    tasks_past_end = Task.objects.exclude(
        status=Task.EXPIRED).filter(end__lte=timezone.now())
    for task_past_end in tasks_past_end:
        task_past_end.status = Task.EXPIRED
        task_past_end.save()


# pylint: disable=not-callable
@celery_task(name="task_has_no_more_occurences")
def task_has_no_more_occurences():
    """
    Set task to expired whose occurence date is less than or equal to today
    """
    # pylint: disable=no-member
    task_occ = TaskOccurrence.objects.exclude(
        task__status=Task.EXPIRED).filter(
            date__gte=date.today()).values_list('task', flat=True)
    tasks = Task.objects.exclude(id__in=task_occ)
    for task in tasks:
        task.status = Task.EXPIRED
        task.save()
