"""
Signals for ona
"""
from django.db.models.signals import post_save, pre_delete

from kaznet.apps.main.models import Task
from kaznet.apps.ona.tasks import (task_auto_create_filtered_data_sets,
                                   task_create_form_webhook)


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


# pylint: disable=unused-argument
def auto_create_ona_filtered_data_sets(sender, instance, created, **kwargs):
    """
    Create ona form filtered data sets
    """
    # only create filtered data sets if it doesn't have filtered data sets
    datasets = instance.json.get('has_filtered_data_sets')
    if not datasets:
        form_id = instance.ona_pk
        project_id = instance.ona_project_id
        title = instance.title
        task_auto_create_filtered_data_sets.delay(
            form_id=form_id, project_id=project_id, form_title=title)


def create_form_webhook_signal(sender, instance, created, **kwargs):
    """
    Signal to create form webhooks
    """
    if not instance.json.get('has_webhook'):
        # only attempt to create webhooks if not already created
        form_id = instance.ona_pk
        task_create_form_webhook.delay(form_id=form_id)


pre_delete.connect(
    delete_xform,
    sender='ona.XForm',
    dispatch_uid='delete_xform')

post_save.connect(
    auto_create_ona_filtered_data_sets,
    sender='ona.XForm',
    dispatch_uid='auto_create_ona_filtered_data_sets'
)

post_save.connect(
    create_form_webhook_signal,
    sender='ona.XForm',
    dispatch_uid='create_form_webhook_signal'
)
