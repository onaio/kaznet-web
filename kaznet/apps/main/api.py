"""
API Methods For Kaznet Main App
"""
from kaznet.apps.main.models import Location, Submission


def validate_task(instance: object):
    """
    Validates Instance Data From Ona
    """
    submission_data = instance.json
    task = instance.xform.task
    user = instance.user
    user_profile = user.userprofile
    # pylint: disable=no-member
    user_submission_count = Submission.objects.filter(
        task=task, user=user).count()
    max_submission = task.user_submission_target
    expertise_requirement = task.required_expertise
    submission_data['bounty'] = task.bounty
    # Submission Review not yet implemented in Ona
    # This might change
    # TODO Update
    if submission_data['_status'] != 'REJECTED':
        # How to validate the coords with the Location
        # ?
        geopoint = submission_data['_geolocation']

        # If Geopoint
        # TODO Figure out how to match geolocation
        # With an actual Location that the task has
        location = Location.objects.get(
            geopoint=geopoint, task=task)
        submission_data['location'] = location

        if location is not None and (
                expertise_requirement is None or
                user_profile.expertise == expertise_requirement):
            if user_submission_count >= max_submission:
                comment = 'Daily Submission Cap for this task has been reached'
                bounty = 0
                submission_data['comments'] = comment
                submission_data['bounty'] = bounty

            submission_data['valid'] = True
            submission_data['status'] = 'a'
    else:
        submission_data['status'] = 'b'
        submission_data['valid'] = True

    # This method will return validated data where by now the data
    # can be processed into a Submission Object
    return submission_data
