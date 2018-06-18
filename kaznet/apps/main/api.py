"""
API Methods For Kaznet Main App
"""
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
    if data['status'] != Submission.REJECTED:
        data = validate_location(data, task)
        if data['status'] != Submission.REJECTED:
            data = validate_submission_time(task, data)

    if data['status'] == Submission.REJECTED:
        validated_data = {
            'task': {
                'type': 'Task',
                'id': task.id
            },
            'user': {
                'type': 'User',
                'id': user.id
            },
            'comments': str(data['comments']),
            'status': Submission.REJECTED,
            'submission_time': data['_submission_time'],
            'valid': False,
            'target_content_type': get_allowed_contenttypes().filter(
                model='instance').first().id,
            'target_id': ona_instance.id
        }

        serializer_instance = KaznetSubmissionSerializer(data=validated_data)
        serializer_instance.is_valid()
        return serializer_instance.save()

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
    serializer_instance.is_valid()
    return serializer_instance.save()


def validate_location(data: dict, task: object):
    """
    Validates Submission Location
    """
    coords = data['_geolocation']
    submission_point = Point(coords[0], coords[1])

    try:
        location = Location.objects.get(
            task=task, shapefile__contains=submission_point)
        data['location'] = location
        data['status'] = Submission.PENDING
        return data
    except Location.DoesNotExist:  # pylint: disable=no-member
        locations = task.locations.all()
        for location in locations:
            if location.geopoint is None:
                # If by any chance a location has no geopoint or shapefile
                data['status'] = Submission.REJECTED
                data['comments'] = INVALID_TASK
                return data

            dist = distance(location.geopoint, submission_point)

            if location.radius is not None:
                if dist <= location.radius:
                    data['location'] = location
                    data['status'] = Submission.PENDING
                    return data

        data['status'] = Submission.REJECTED
        data['comments'] = INCORRECT_LOCATION
        return data


def validate_user(data: dict, task: object, user: object):
    """
    Validates that the user can submit to this
    task
    """
    user_expertise = user.userprofile.expertise

    if task.required_expertise < user_expertise:
        data['status'] = Submission.PENDING
        return data

    data['status'] = Submission.REJECTED
    data['comments'] = LACKING_EXPERTISE
    return data


def validate_submission_time(task: object, data: dict):
    """
    Validates that the user submitted at right
    time
    """
    submission_time = dateutil.parser.parse(data['_submission_time'])

    if TaskOccurrence.objects.filter(  # pylint: disable=no-member
            task=task).filter(
                date__exact=submission_time.date()).filter(
                    start_time__lte=submission_time.time()).filter(
                        end_time__gte=submission_time.time()).exists():
        data['status'] = Submission.PENDING
        return data

    data['status'] = Submission.REJECTED
    data['comments'] = INVALID_SUBMISSION_TIME
    return data
