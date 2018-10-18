"""
Celery tasks module for main Kaznet app
"""

from celery import task as celery_task
from django.utils import timezone
from datetime import datetime

from kaznet.apps.main.api import (create_submission,
                                  task_set_end_date_passed,
                                  task_occurence_passed)
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


@celery_task(name="task_end_date_passed")  # pylint: disable=not-callable
def task_set_end_date_passed():
    """
    Sets Task to expired if end date is in the past or today
    """
    tasks_past_end = Task.objects.exclude(
        status=Task.EXPIRED).filter(end__lte=timezone.now())
    for task_past_end in tasks_past_end:
        task_past_end.status = Task.EXPIRED
        task_past_end.save()


@celery_task(name="task_has_no_more_occurences")  # pylint: disable=not-callable
def task_occurences_past_date():
    """
    Set task to expired whose occurence date is less than or equal to today
    """
    no_occurence_in_future = Task.objects.exclude(
        taskoccurrence__date__gte=datetime.today())
    for no_occurence in no_occurence_in_future:
        no_occurence.status = Task.EXPIRED
        no_occurence.save()
    
    
