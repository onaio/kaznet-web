"""
Signals for tasking
"""
from django.db.models.signals import post_save

from tasking.utils import generate_task_occurrences

from kaznet.apps.main.models import TaskOccurrence


# pylint: disable=unused-argument
def create_occurrences(sender, instance, created, **kwargs):
    """
    Create occurrences when a task timing_rule changes
    """
    if instance.timing_rule:
        # delete any existing occurrences
        instance.taskoccurrence_set.all().delete()
        # generate new occurrences
        generate_task_occurrences(
            instance, OccurrenceModelClass=TaskOccurrence)


post_save.connect(
    create_occurrences,
    sender='main.Task',
    dispatch_uid='create_task_occurrences')
