"""
Signals for tasking
"""
from django.db.models.signals import post_save

from tasking.utils import generate_task_occurrences

from kaznet.apps.main.models import TaskOccurrence
from kaznet.apps.main.models import Submission

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

def create_submission(sender, instance, created, **kwargs):
    """
    Create a kaznet.apps.main submission after a
    kaznet.apps.ona submission is created
    """
    task = instance.get_task()
    if task is not None:
        bounty = task.bounty_set.all().order_by('-created').first()
        submission = Submission(
            task=task,
            bounty=bounty,
            location=None, # TODO: in different PR
            # TODO: what if dict lacks some keys
            submission_time=instance.json["submission_time"],
            user_id=instance.json["user_id"]
        )
        submission.save()


post_save.connect(
    create_occurrences,
    sender='main.Task',
    dispatch_uid='create_task_occurrences')

post_save.connect(
    create_submission,
    sender='ona.OnaInstance',
    dispatch_uid='create_kaznet_main_submission')
