"""
utils module for Ona app
"""
from django.db import transaction
from django.db.models import Q

from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.models import Submission
from kaznet.apps.ona.models import Instance, XForm


@transaction.atomic
def delete_instance(instance: object):
    """
    This method attempts to cleanly delete an Onadata Instance as well as all
    associated Submissions.  The entire transaction is atomic and is only
    successfully committed to the database when everything PASSES
    """
    # get the instance contenttype
    instance_type = get_allowed_contenttypes().filter(model='instance').first()
    # get all related submissions
    submissions = Submission.objects.filter(  # pylint: disable=no-member
        target_object_id=instance.id,
        target_content_type=instance_type
    )
    # delete submissions in a way that signals are sent
    for submission in submissions:
        submission.delete()
    # finally, delete the instance itself
    instance.delete()


@transaction.atomic
def delete_xform(xform: object):
    """
    This method attempts to cleanly delete an Onadata XForm as well as all
    associated Instances and Submissions.  The entire transaction is atomic
    and is only successfully committed to the database when everything PASSES
    """
    # get all Instances
    # pylint: disable=no-member
    instances = Instance.objects.filter(xform=xform)
    # delete all instances and submissions safely
    for instance in instances:
        delete_instance(instance)
    # finally delete the XForm in a way that singals are sent
    xform.delete()


@transaction.atomic
def delete_project(project: object):
    """
    This method attempts to cleanly delete an Onadata Project as well as all
    associated XForms, Instances and Submissions.  The entire transaction is
    atomic and is only successfully committed to the database when everything
    PASSES
    """
    # get all XForms
    xforms = XForm.objects.filter(  # pylint: disable=no-member
        Q(ona_project_id=project.ona_pk) | Q(project=project))
    # delete all XForms safely
    for xform in xforms:
        delete_xform(xform)
    # finally delete the Project in a way that signals are called
    project.delete()
