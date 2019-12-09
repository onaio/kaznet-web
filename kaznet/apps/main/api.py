"""
API Methods For Kaznet Main App
"""
import logging
from datetime import datetime

from django.conf import settings
from django.contrib.gis.geos import Point

import dateutil.parser
import pytz
from geopy.distance import distance
from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.common_tags import (INCORRECT_LOCATION,
                                          INVALID_SUBMISSION_TIME,
                                          SUBMISSION_TIME,
                                          LACKING_EXPERTISE,
                                          SUBMISSIONS_MORE_THAN_LIMIT,
                                          START_TIME, END_TIME,
                                          INVALID_COLLECTION_TIME)
from kaznet.apps.main.models import (Location, Submission, TaskLocation,
                                     TaskOccurrence)
from kaznet.apps.main.serializers import KaznetSubmissionSerializer
from kaznet.apps.ona.api import convert_ona_to_kaznet_submission_status
from kaznet.apps.ona.tasks import task_sync_submission_review

# Get an instance of a logger
LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-branches


def create_submission(ona_instance: object):
    """
    Validates Submission Data and Creates a Submission
    """
    data = ona_instance.json
    task = ona_instance.get_task()
    instance_id = ona_instance.id

    # don't create a submission for missing task
    if task is None:
        # log error then exit this function
        LOGGER.error(
            "Instance: %d belongs to a task that has been deleted",
            ona_instance.id)
        return None

    validated_data = validate_submission_data(ona_instance)

    # Approve submission if Auto Approval is turned on
    # and Submission is pending review
    if validated_data['status'] == Submission.PENDING and \
            settings.SUBMISSION_AUTO_APPROVAL:
        validated_data['status'] = Submission.APPROVED

    # call sync_submission_review based on validated_data[status]
    # and the json field
    task_sync_submission_review.delay(
        ona_instance.id,
        validated_data['status'],
        validated_data['comments'])

    if 'location' not in validated_data:
        location = get_locations(
            data.get(settings.ONA_GEOLOCATION_FIELD), task)
        if location:
            # get one of the valid locations
            validated_data['location'] = {
                'type': 'Location',
                'id': location.first().id
            }

    validated_data['valid'] = not validated_data['status'] == \
        Submission.REJECTED

    # Get submission tied to instance_id if present and update it else
    # create a new submission
    submission = Submission.objects.filter(  # pylint: disable=no-member
        target_object_id=instance_id).first()
    serializer_instance = KaznetSubmissionSerializer(
        submission, data=validated_data)
    if serializer_instance.is_valid():
        return serializer_instance.save()
    return None


def validate_submission_data(ona_instance: object):
    """Validates submission data making sure the submission
    was submitted by a valid user who has not reached their submission limit
    for a task and that the submission was submitted at the
    right location and time
    """
    data = ona_instance.json
    task = ona_instance.get_task()
    user = ona_instance.user

    validated_data = {
        'task': {
            'type': 'Task',
            'id': task.id
        },
        'user': {
            'type': 'User',
            'id': user.id
        },
        'submission_time': data['_submission_time'],
        'valid': False,
        'target_content_type': get_allowed_contenttypes().filter(
            model='instance').first().id,
        'target_id': ona_instance.id
    }

    if task.bounty is not None:
        validated_data['bounty'] = {
            'type': 'Bounty',
            'id': task.bounty.id
        }

    status = Submission.PENDING
    comment = ''

    # if submission has had a review, update status and comments appropriately
    if settings.ONA_STATUS_FIELD in data:
        status = convert_ona_to_kaznet_submission_status(
            ona_status=data[settings.ONA_STATUS_FIELD])
        comment = str(
            data.get(settings.ONA_COMMENTS_FIELD, ""))
        # indicate that the instance object's review status
        # has already been synced
        ona_instance.json["synced_with_ona_data"] = True

    if status == Submission.PENDING:
        status, comment = validate_user(task, user)

        # If the person submitting the data is a valid user
        # Validate that they havent reached their submission limit
        if status != Submission.REJECTED:
            status, comment = validate_submission_limit(task, user)

        if status != Submission.REJECTED:
            status, comment = validate_submission_time(task, data)

        if status != Submission.REJECTED and \
                all(data[settings.ONA_GEOLOCATION_FIELD]):
            location, status, comment = validate_location(
                data[settings.ONA_GEOLOCATION_FIELD], task)
            if location:
                validated_data['location'] = {
                    'type': 'Location',
                    'id': location.id
                }

    validated_data['status'] = status
    validated_data['comments'] = str(comment)

    return validated_data


def get_locations(coords: list, task: object):
    """
    Return the location given the instance data and task object
    """
    # Check if we were able to successfully get coords
    # If we weren't then return None
    if coords and all(coords):
        # Expects coords to be passed in as latitude, longitude
        submission_point = Point(coords[1], coords[0])

        # get task locations with a shapefile that has the submission_point
        # within its range

        # pylint: disable=no-member
        task_locations = TaskLocation.objects.filter(
            task=task, location__shapefile__contains=submission_point).\
            values_list('location', flat=True)
        if task_locations:
            return Location.objects.filter(id__in=task_locations)
        return task.locations.exclude(geopoint=None, radius=None)
    return task.locations.none()


def validate_location(coords: list, task: object):
    """
    Validates Submission Location
    """
    locations = get_locations(coords, task)
    # Onadata endpoint passes coordinates as Latitude, Longitude
    # Point takes in coordinates as Longitude, Latitude
    # Ref: https://docs.djangoproject.com/en/2.2/ref/contrib/gis/geos/
    submission_point = Point(coords[1], coords[0])

    if locations:
        for location in locations:
            # validate using radius and geopoint
            if location.radius and location.geopoint:
                # distance in meters
                dist = distance(location.geopoint, submission_point).m
                if dist <= location.radius:
                    return (location, Submission.PENDING, "")

            # incase location has shapefile instead, use shapefile
            if location.shapefile:
                return (location, Submission.PENDING, "")

        # if location is not valid reject
        return (None, Submission.REJECTED, INCORRECT_LOCATION)
    # if provided location is not in task locations, reject
    return (None, Submission.REJECTED, INCORRECT_LOCATION)


def validate_user(task: object, user: object):
    """
    Validates that the user can submit to this
    task
    """
    user_expertise = user.userprofile.expertise

    # Check if the User submitting Data has an expertise level
    # above or equal to the required_expertise
    if int(task.required_expertise) <= int(user_expertise):
        return (Submission.PENDING, "")

    # Reject the data if user doesn't meet the requirements
    return (Submission.REJECTED, LACKING_EXPERTISE)


def validate_submission_time(task: object, submission_data: dict):
    """Validate that the time a submission was made is within the acceptable
    range utilizing the start and end date if present else using the
    submission_time
    """
    # pylint: disable=no-else-return
    if (submission_data.get(START_TIME) and submission_data.get(END_TIME)):
        submission_start = submission_data.get(START_TIME)
        submission_end = submission_data.get(END_TIME)

        return (Submission.PENDING, '') if \
            validate_within_task_occurrence(task, submission_start) and \
            validate_within_task_occurrence(task, submission_end) else \
            (Submission.REJECTED, INVALID_COLLECTION_TIME)
    else:
        submitted_at = submission_data.get(SUBMISSION_TIME)

        return (Submission.PENDING, '') if \
            validate_within_task_occurrence(task, submitted_at) \
            else (Submission.REJECTED, INVALID_SUBMISSION_TIME)


def validate_within_task_occurrence(task: object, time: str):
    """
    Validates that a passed in time string is within the Task Occurrence
    range of a task
    """
    # We turn the isoformated string we get from Instance data into
    # a datetime object for easier comparison
    try:
        time = dateutil.parser.parse(time)
    except ValueError:
        pass  # not a valid datetime string
    else:
        # Check if the time is of proper timezone when compared
        # to one of the tasks datetimes
        if settings.TIME_ZONE:
            timezone = pytz.timezone(settings.TIME_ZONE)

            if time.tzinfo:
                time = time.astimezone(timezone)
            else:
                now = datetime.now(timezone)
                time = time + now.utcoffset()

        # We query all TaskOccurrence Objects for the Task
        # To see if the time is within the acceptable range
        if TaskOccurrence.objects.filter(  # pylint: disable=no-member
                task=task).filter(
                    date__day=time.day,
                    date__month=time.month,
                    date__year=time.year
                    ).filter(
                        start_time__lte=time.time()).filter(
                            end_time__gte=time.time()).exists():
            return True
    # We return false if there was no TaskOccurence within the time
    return False


def validate_submission_limit(task: object, user: object):
    """
    Validates that the user submissions are within the allowed submissions
    limit of a task
    """
    # pylint: disable=no-member
    limit = task.user_submission_target
    user_submissions = Submission.objects.filter(
        task_id=task.id, user_id=user.id).count()

    if limit is not None:
        # Check if the number of submissions for this task exceed
        # the limit set
        if user_submissions > limit:
            return (Submission.REJECTED, SUBMISSIONS_MORE_THAN_LIMIT)
    return (Submission.PENDING, "")
