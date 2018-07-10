"""
Signals for tasking
"""
from django.db.models.signals import post_save

from kaznet.apps.main.tasks import (task_create_occurrences,
                                    task_create_submission)


# pylint: disable=unused-argument
def create_occurrences(sender, instance, created, **kwargs):
    """
    Create occurrences when a task is saved
    """
    task_create_occurrences.delay(task_id=instance.id)


def create_submission(sender, instance, created, **kwargs):
    """
    Create a kaznet.apps.main submission after a
    kaznet.apps.ona submission is created
    """
    task_create_submission.delay(instance_id=instance.id)


post_save.connect(
    create_occurrences,
    sender='main.Task',
    dispatch_uid='create_task_occurrences')

post_save.connect(
    create_submission,
    sender='ona.Instance',
    dispatch_uid='create_kaznet_main_submission')
