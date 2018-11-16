"""
Signals for ona
"""
from django.conf import settings
from django.db.models.signals import post_save, pre_delete

from kaznet.apps.main.common_tags import (HAS_FILTERED_DATASETS_FIELD_NAME,
                                          HAS_WEBHOOK_FIELD_NAME)
from kaznet.apps.main.models import Task
from kaznet.apps.ona.models import Instance, XForm
from kaznet.apps.ona.tasks import (task_auto_create_filtered_data_sets,
                                   task_create_form_webhook)


# pylint: disable=unused-argument
def delete_xform(sender, instance, **kwargs):
    """
    Pre delete signal handler for XForm objects
    """
    # get the task
    task = instance.task
    if task is not None:
        # we need to mark the task as draft because it no longer has a form
        task.status = Task.DRAFT
        task.target_content_object = None
        task.save()

        # delete submissions in a way that signals are called
        for sub in task.submission_set.all():
            sub.delete()


def delete_project(sender, instance, **kwargs):
    """
    Predelete signal handler for Project objects
    """
    # delete any Instances in a way that signals are called
    ona_instances = Instance.objects.filter(xform__project=instance)
    for ona_instance in ona_instances:
        ona_instance.delete()
    # delete any XForms in a way that signals are called
    xforms = XForm.objects.filter(project=instance)
    for xform in xforms:
        xform.delete()


# pylint: disable=unused-argument
def auto_create_ona_filtered_data_sets(sender, instance, created, **kwargs):
    """
    Create ona form filtered data sets
    """
    # only create filtered data sets if it doesn't have filtered data sets
    if not instance.json.get(HAS_FILTERED_DATASETS_FIELD_NAME) and \
            settings.AUTO_CREATE_FILTERED_DATASETS:
        form_id = instance.ona_pk
        project_id = instance.ona_project_id
        title = instance.title
        task_auto_create_filtered_data_sets.delay(
            form_id=form_id, project_id=project_id, form_title=title)


def create_form_webhook_signal(sender, instance, created, **kwargs):
    """
    Signal to create form webhooks
    """
    # only attempt to create webhooks if not already created
    if not instance.json.get(HAS_WEBHOOK_FIELD_NAME) and \
            settings.AUTO_CREATE_SUBMISSION_WEBHOOKS:
        form_id = instance.ona_pk
        task_create_form_webhook.delay(form_id=form_id)


pre_delete.connect(
    delete_xform,
    sender='ona.XForm',
    dispatch_uid='delete_xform')

pre_delete.connect(
    delete_project,
    sender='ona.Project',
    dispatch_uid='delete_project')

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
