"""
API Methods For Kaznet Main App
"""
from django.conf import settings
from django.contrib.gis.geos import Point

import logging
import dateutil.parser
from geopy.distance import distance
from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.common_tags import (INCORRECT_LOCATION,
                                          INVALID_SUBMISSION_TIME,
                                          LACKING_EXPERTISE,
                                          SUBMISSIONS_MORE_THAN_LIMIT)
from kaznet.apps.main.models import Location, Submission, TaskOccurrence, \
    TaskLocation
from kaznet.apps.main.serializers import KaznetSubmissionSerializer
from kaznet.apps.ona.tasks import task_sync_submission_review
from kaznet.apps.ona.api import convert_ona_to_kaznet_submission_status


# Get an instance of a logger
LOGGER = logging.getLogger("submission logger")

# pylint: disable=too-many-branches


def create_submission(ona_instance: object):
    """
    Validates Submission Data and Creates a Submission
    """
    data = ona_instance.json
    task = ona_instance.get_task()
    user = ona_instance.user

    # don't create a submission for missing task
    if task is None:
        # log error then exit this function
        LOGGER.error(
            "Instance: %d belongs to a task that has been deleted",
            ona_instance.id)
        return None

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

    # if submission has had a review, update validated_data appropriately
    if settings.ONA_STATUS_FIELD in data:
        validated_data['status'] = convert_ona_to_kaznet_submission_status(
            ona_status=data[settings.ONA_STATUS_FIELD])
        validated_data['comments'] = str(
            data.get(settings.ONA_COMMENTS_FIELD, ""))
        # indicate that the instance object's review status
        # has already been synced
        ona_instance.json["synced_with_ona_data"] = True

    # if submission hasn't had a review(pending), or no review information of
    # submission
    if settings.ONA_STATUS_FIELD not in data or (
            validated_data['status'] == Submission.PENDING and
            not validated_data['comments']):
        # Validation: order: User - Location - Time
        status, comment = validate_user(task, user)
        validated_data['status'] = status
        validated_data['comments'] = str(comment)

        # Validate location if submission passed user validation and
        # submission has location details
        if validated_data['status'] != Submission.REJECTED and \
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

            # Validate time if Submission passed location validation
            if validated_data['status'] != Submission.REJECTED:
                status, comment = validate_submission_time(
                    task, data['_submission_time'])
                validated_data['status'] = status
                validated_data['comments'] = str(comment)

                # Validate limit if submission passed time validation
                if validated_data['status'] != Submission.REJECTED:
                    status, comment = validate_submission_limit(task, user)

                    # Auto approve submission if it passes all validations and
                    #  auto approval is set
                    if status == Submission.PENDING and \
                            settings.SUBMISSION_AUTO_APPROVAL:
                        validated_data['status'] = Submission.APPROVED
                        validated_data['comments'] = str(comment)
                    else:
                        validated_data['status'] = status
                        validated_data['comments'] = str(comment)

    if 'location' not in validated_data:
        location = get_locations(
            data.get(settings.ONA_GEOLOCATION_FIELD), task)
        if location:
            # get one of the valid locations
            validated_data['location'] = {
                'type': 'Location',
                'id': location.first().id
            }

    # call sync_submission_review based on validated_data[status]
    #  and the json field
    task_sync_submission_review.delay(
        ona_instance.id, validated_data['status'], validated_data['comments'])

    if validated_data['status'] == Submission.REJECTED:
        validated_data['valid'] = False
    else:
        validated_data['valid'] = True
    serializer_instance = KaznetSubmissionSerializer(data=validated_data)
    if serializer_instance.is_valid():
        return serializer_instance.save()
    return None


def get_locations(coords: list, task: object):
    """
    Return the location given the instance data and task object
    """
    # Check if we were able to successfully get coords
    # If we weren't then return None
    if coords and all(coords):
        submission_point = Point(coords[0], coords[1])

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
    submission_point = Point(coords[0], coords[1])

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


def validate_submission_time(task: object, submission_time: str):
    """
    Validates that the user submitted at right time
    """
    # We turn the isoformated string we get from Instance data into
    # a datetime object for easier comparison
    try:
        submission_time = dateutil.parser.parse(submission_time)
    except ValueError:
        pass  # not a valid datetime string
    else:
        # We query all TaskOccurrence Objects for the Submissions Task
        # To see if the user submitted the data at an acceptable time range
        if TaskOccurrence.objects.filter(  # pylint: disable=no-member
                task=task).filter(
                    date__day=submission_time.day,
                    date__month=submission_time.month,
                    date__year=submission_time.year
                ).filter(start_time__lte=submission_time
                         .time()).filter(end_time__gte=submission_time
                                         .time()).exists():
            return (Submission.PENDING, "")
    # We reject the submission if there was no TaskOccurrence
    # That match the submission_time
    return (Submission.REJECTED, INVALID_SUBMISSION_TIME)


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
