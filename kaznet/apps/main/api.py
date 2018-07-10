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
                                          INVALID_TASK, LACKING_EXPERTISE)
from kaznet.apps.main.models import Location, Submission, TaskOccurrence
from kaznet.apps.main.serializers import KaznetSubmissionSerializer


def create_submission(ona_instance: object):
    """
    Validates Submission Data and Creates a Submission
    """
    data = ona_instance.json
    task = ona_instance.get_task()
    user = ona_instance.user

    data = validate_user(data, task, user)
    if data[settings.ONA_STATUS_FIELD] != Submission.REJECTED:
        data = validate_location(data, task)
        if data[settings.ONA_STATUS_FIELD] != Submission.REJECTED:
            data = validate_submission_time(task, data)

    if data[settings.ONA_STATUS_FIELD] == Submission.REJECTED:
        validated_data = {
            'task': {
                'type': 'Task',
                'id': task.id
            },
            'user': {
                'type': 'User',
                'id': user.id
            },
            'comments': str(data[settings.ONA_COMMENTS_FIELD]),
            'status': Submission.REJECTED,
            'submission_time': data['_submission_time'],
            'valid': False,
            'target_content_type': get_allowed_contenttypes().filter(
                model='instance').first().id,
            'target_id': ona_instance.id
        }

        serializer_instance = KaznetSubmissionSerializer(data=validated_data)
        if serializer_instance.is_valid():
            return serializer_instance.save()
        return None

    data = {
        'task': {
            'type': 'Task',
            'id': task.id
        },
        'user': {
            'type': 'User',
            'id': user.id
        },
        'location': {
            'type': 'Location',
            'id': data['location'].id
        },
        'bounty': {
            'type': 'Bounty',
            'id': task.bounty.id
        },
        'status': Submission.PENDING,
        'submission_time': data['_submission_time'],
        'valid': True,
        'target_content_type': get_allowed_contenttypes().filter(
            model='instance').first().id,
        'target_id': ona_instance.id
    }

    serializer_instance = KaznetSubmissionSerializer(data=data)
    if serializer_instance.is_valid():
        return serializer_instance.save()
    return None


def validate_location(data: dict, task: object):
    """
    Validates Submission Location
    """
    coords = data.get('_geolocation')

    # Check if we were able to succesfully get coords
    # If we weren't then the Submission is not Valid
    if coords and all(coords):
        submission_point = Point(coords[0], coords[1])

        try:
            # Check if there is any location with a shapefile
            # that has the submission_point within its range
            location = Location.objects.get(
                task=task, shapefile__contains=submission_point)
        except Location.DoesNotExist:  # pylint: disable=no-member
            locations = task.locations.all()
            for location in locations:
                if location.geopoint is None:
                    # If by any chance a location has no geopoint or shapefile
                    # we reject the submission
                    data[settings.ONA_STATUS_FIELD] = Submission.REJECTED
                    data[settings.ONA_COMMENTS_FIELD] = INVALID_TASK
                    return data

                dist = distance(location.geopoint, submission_point)

                if location.radius is not None:
                    if dist <= location.radius:
                        data['location'] = location
                        data[settings.ONA_STATUS_FIELD] = Submission.PENDING
                        return data

            # Reject Submission if there is no location for the task
            # that matches there submission_point
            data[settings.ONA_STATUS_FIELD] = Submission.REJECTED
            data[settings.ONA_COMMENTS_FIELD] = INCORRECT_LOCATION
            return data
        else:
            data['location'] = location
            data[settings.ONA_STATUS_FIELD] = Submission.PENDING
            return data

    # Add Rejected status to Submission since it doesn't
    # any location data thus is in valid
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
    if task.required_expertise <= user_expertise:
        data[settings.ONA_STATUS_FIELD] = Submission.PENDING
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
    submission_time = dateutil.parser.parse(data['_submission_time'])

    # We query all TaskOccurence Objects for the Submissions Task
    # To see if the user submitted the data at an acceptable time range
    if TaskOccurrence.objects.filter(  # pylint: disable=no-member
            task=task).filter(
                date__exact=submission_time.date()).filter(
                    start_time__lte=submission_time.time()).filter(
                        end_time__gte=submission_time.time()).exists():
        data[settings.ONA_STATUS_FIELD] = Submission.PENDING
        return data

    # We reject the submission if there was no TaskOccurence
    # That match the submission_time
    data[settings.ONA_STATUS_FIELD] = Submission.REJECTED
    data[settings.ONA_COMMENTS_FIELD] = INVALID_SUBMISSION_TIME
    return data
