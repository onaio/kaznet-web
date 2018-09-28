"""
API Methods For Kaznet Main App
"""
from django.conf import settings
from django.contrib.gis.geos import Point

import dateutil.parser
from geopy.distance import distance
from tasking.utils import get_allowed_contenttypes

from kaznet.apps.main.common_tags import (INCORRECT_LOCATION,
                                          INVALID_SUBMISSION_TIME,
                                          LACKING_EXPERTISE)
from kaznet.apps.main.models import Location, Submission, TaskOccurrence, \
    TaskLocation
from kaznet.apps.main.serializers import KaznetSubmissionSerializer


def create_submission(ona_instance: object):
    """
    Validates Submission Data and Creates a Submission
    """
    data = ona_instance.json
    task = ona_instance.get_task()
    user = ona_instance.user

    # Check if submission has had a review
    if settings.ONA_STATUS_FIELD in data:
        # Order of validation: User - Location - Time
        # only perform validation if the submission is pending and
        # has no comment
        if (data[settings.ONA_STATUS_FIELD] ==
            settings.ONA_SUBMISSION_REVIEW_PENDING or
            data[settings.ONA_STATUS_FIELD] == Submission.PENDING) and \
                (data[settings.ONA_COMMENTS_FIELD] == "" or
                 not data[settings.ONA_COMMENTS_FIELD]):
            data = validate_user(data, task, user)

            # Validate location if user validation was successful
            if data[settings.ONA_STATUS_FIELD] != Submission.REJECTED and \
                    all(data[settings.ONA_GEOLOCATION_FIELD]):
                data = validate_location(data, task)

                # Validate time if location validation was successful
                if data[settings.ONA_STATUS_FIELD] != Submission.REJECTED:
                    data = validate_submission_time(task, data)

                    # Auto Approve if auto approve is set else kep it pending
                    if data[settings.ONA_STATUS_FIELD] != Submission.REJECTED \
                            and settings.SUBMISSION_AUTO_APPROVAL:
                        data[settings.ONA_STATUS_FIELD] = Submission.APPROVED
                    elif data[settings.ONA_STATUS_FIELD] != \
                            Submission.REJECTED:
                        data[settings.ONA_STATUS_FIELD] = Submission.PENDING

        else:
            location = get_locations(
                data[settings.ONA_GEOLOCATION_FIELD], task)
            if location:
                # get one of the valid locations
                data['location'] = location.first()

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
        if 'location' in data:
            validated_data['location'] = {
                'type': 'Location',
                'id': data['location'].id
            }
        if data[settings.ONA_STATUS_FIELD] == Submission.REJECTED or \
                data[settings.ONA_STATUS_FIELD] == \
                settings.ONA_SUBMISSION_REVIEW_REJECTED:

            validated_data['comments'] = str(data[settings.ONA_COMMENTS_FIELD])
            validated_data['status'] = Submission.REJECTED
        else:
            validated_data['bounty'] = {
                'type': 'Bounty',
                'id': task.bounty.id
            }
            validated_data['status'] = convert_ona_kaznet_submission_status(
                data[settings.ONA_STATUS_FIELD])
            validated_data['comments'] = str(data[settings.ONA_COMMENTS_FIELD])
            validated_data['valid'] = True
    else:
        validated_data = data

    serializer_instance = KaznetSubmissionSerializer(data=validated_data)
    if serializer_instance.is_valid():
        return serializer_instance.save()
    return None


def convert_ona_kaznet_submission_status(ona_status: str):
    """
    Convert Ona Instance statuses (1, 2, 3) to kaznet submission statuses
    """
    if ona_status == settings.ONA_SUBMISSION_REVIEW_APPROVED:
        return Submission.APPROVED
    if ona_status == settings.ONA_SUBMISSION_REVIEW_REJECTED:
        return Submission.REJECTED
    if ona_status == settings.ONA_SUBMISSION_REVIEW_PENDING:
        return Submission.PENDING
    return None


def get_locations(coords: list, task: object):
    """
    Return the location given the instance data and task object
    """
    # Check if we were able to succesfully get coords
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


def validate_location(data: dict, task: object):
    """
    Validates Submission Location
    """
    coords = data.get('_geolocation')
    locations = get_locations(coords, task)
    submission_point = Point(coords[0], coords[1])

    if locations:
        for location in locations:
            if location.radius and location.geopoint:
                # distance in meters
                dist = distance(location.geopoint, submission_point).m
                if dist <= location.radius:
                    data['location'] = location
                    return data

                data[settings.ONA_STATUS_FIELD] = Submission.REJECTED
                data[settings.ONA_COMMENTS_FIELD] = INCORRECT_LOCATION
            # incase location has shapefile instead
            data['location'] = location
            return data

    # if provided location is not in task locations, reject
    data[settings.ONA_STATUS_FIELD] = Submission.REJECTED
    data[settings.ONA_COMMENTS_FIELD] = INCORRECT_LOCATION
    return data


def validate_user(data: dict, task: object, user: object):
    """
    Validates that the user can submit to this
    task
    """
    user_expertise = user.userprofile.expertise

    # Check if the User submitting Data has an expertise level
    # above or equal to the required_expertise
    if int(task.required_expertise) <= int(user_expertise):
        return data

    # Reject the data if user doesn't meet the requirements
    data[settings.ONA_STATUS_FIELD] = Submission.REJECTED
    data[settings.ONA_COMMENTS_FIELD] = LACKING_EXPERTISE
    return data


def validate_submission_time(task: object, data: dict):
    """
    Validates that the user submitted at right
    time
    """
    # We turn the isoformated string we get from Instance data into
    # a datetime object for easier comparison
    try:
        submission_time = dateutil.parser.parse(data['_submission_time'])
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
                ).filter(
                    start_time__lte=submission_time.time()).filter(
                        end_time__gte=submission_time.time()).exists():
            return data
    # We reject the submission if there was no TaskOccurence
    # That match the submission_time
    data[settings.ONA_STATUS_FIELD] = Submission.REJECTED
    data[settings.ONA_COMMENTS_FIELD] = INVALID_SUBMISSION_TIME
    return data
