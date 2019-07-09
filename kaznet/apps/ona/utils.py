"""
utils module for Ona app
"""
from django.db import transaction
from django.db.models import Q
from django.conf import settings

from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.models import Submission
from kaznet.apps.ona.models import Instance, XForm, Project


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


def check_if_users_can_submit_to_form(xform: object):
    """
    Checks if users can make submissions to the XForm

    The check is done by checking that the XForm belongs to an Ona Project
    which has members of the `settings.ONA_ORG_NAME` organization with at least
    the `dataentry` Onadata role. It allows users to make submissions if they are :
    dataentry, editor, or manager
    """
    if xform.json.get("owner") != settings.ONA_ORG_NAME:
        # the form does not have the expected owner
        xform.json[settings.ONA_XFORM_CONFIGURED_FIELD] = XForm.WRONG_OWNER
    elif xform.ona_project_id:
        try:
            the_project = Project.objects.get(ona_pk=xform.ona_project_id)
        except Project.DoesNotExist:  # pylint:disable=no-member
            # the XForm has no valid Project
            xform.json[settings.ONA_XFORM_CONFIGURED_FIELD] = XForm.NO_PROJECT
        else:
            expected_org = settings.ONA_ORG_NAME
            expected_team_name = f"{expected_org}#members"
            # find the team on the project
            project_teams = the_project.json.get("teams")
            if project_teams:
                the_team = None
                for entry in project_teams:
                    if entry["name"] == expected_team_name:
                        the_team = entry

                if the_team is None:
                    # we didn't find a valid team
                    xform.json[
                        settings.ONA_XFORM_CONFIGURED_FIELD] =\
                            XForm.NO_VALID_TEAM
                elif the_team['role'] in [settings.ONA_CONTRIBUTER_ROLE, "manager", "editor"]:
                    # its valid, everything is good
                    xform.json[settings.ONA_XFORM_CONFIGURED_FIELD] =\
                        XForm.CORRECTLY_CONFIGURED
                else:
                    # not right, contributors will not be able to submit data
                    xform.json[settings.ONA_XFORM_CONFIGURED_FIELD] =\
                        XForm.MEMBERS_CANT_SUBMIT
            else:
                # the project has no teams
                xform.json[settings.ONA_XFORM_CONFIGURED_FIELD] =\
                    XForm.NO_TEAMS_AT_ALL
    else:
        # the XForm has no valid Project
        xform.json[settings.ONA_XFORM_CONFIGURED_FIELD] = XForm.NO_PROJECT

    xform.save()
    return xform
