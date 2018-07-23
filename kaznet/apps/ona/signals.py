"""
Signals for ona
"""
from django.db.models.signals import pre_delete

from kaznet.apps.main.models import Task


# pylint: disable=unused-argument
def delete_xform(sender, instance, **kwargs):
    """
    Pre delete signal handler for XForm objects
    """
    # get the task
    task = instance.task.first()
    if task is not None:
        task.status = Task.DRAFT
        task.target_content_object = None
        task.save()


pre_delete.connect(
    delete_xform,
    sender='ona.XForm',
    dispatch_uid='delete_xform')
