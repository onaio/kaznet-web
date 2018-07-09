"""
Signals for tasking
"""
from django.db.models.signals import post_save

from kaznet.apps.main.models import Submission
from kaznet.apps.main.tasks import task_create_occurrences


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
    task = instance.get_task()
    submission_time = instance.json.get("submission_time")
    user = instance.user

    if all([task, submission_time, user]):
        bounty = task.bounty_set.all().order_by('-created').first()
        submission = Submission(
            task=task,
            bounty=bounty,
            location=None,
            submission_time=submission_time,
            user=user
        )
        submission.save()


post_save.connect(
    create_occurrences,
    sender='main.Task',
    dispatch_uid='create_task_occurrences')

post_save.connect(
    create_submission,
    sender='ona.Instance',
    dispatch_uid='create_kaznet_main_submission')
