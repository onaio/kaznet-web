"""
API Methods For Kaznet Main App
"""
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


def validate_instance_location(ona_instance: object):
    """
    Validates Instances Location
    for task
    """
    data = ona_instance.json
    task = ona_instance.xform.task
    coords = ona_instance['_geolocation']
    location = None
    submission_point = Point(coords[0], coords[1])

    if task.locations is not None:
        # Search for a location within the task possible locations
        # Where the submission_point is within
        # TODO Only checks geopoint, ADD a check for shapefile

        # TODO is radius in metres or Kilometres
        # How to get all valid radius for the location ???
        radius_list = get_task_location_radius(task)

        for radius in radius_list:
            # Chance of getting two locations ??? Maybe ?
            location = task.locations.filter(
                geopoint__distance_lte=(
                    submission_point, Distance(m=radius)))

        if location is not None:
            validated_data = data.copy()
            validated_data['location'] = location
            validated_data['valid'] = True

            return validated_data

        validated_data = data.copy()
        validated_data['valid'] = False
        validated_data['comments'] = 'Submitted at wrong location.'

        return validated_data

    # No Locations on Task..
    # Assume Task doesn't care about location and validate Submission
    # After this method is called data will probably go through some other kind
    # of validation
    validated_data = data.copy()
    validated_data['valid'] = True
    return validated_data


def get_task_location_radius(task: object):
    """
    Yields the radiuses for all locations of a particular
    task
    """
    locations = task.locations.all()

    for location in locations:
        yield location.radius
