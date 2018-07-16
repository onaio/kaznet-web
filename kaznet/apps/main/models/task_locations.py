"""
TaskLocation models module
"""
from django.db import models

from tasking.models import BaseTaskLocation


class TaskLocation(BaseTaskLocation):
    """
    Provides extra information on Task-Location relationship
    """
    task = models.ForeignKey("main.Task", on_delete=models.CASCADE)
    location = models.ForeignKey("main.Location", on_delete=models.CASCADE)

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskLocation
        """
        abstract = False
        app_label = 'main'
        ordering = ['task', 'location', 'start']

    def __str__(self):
        """
        String representation of a TaskLocation object
        """
        return f"{self.task.name} at {self.location.name}"

    def get_location_name(self):
        if self.location:
            return self.location.name
        return None

    def get_location_description(self):
        if self.location:
            return self.location.description
        return None

    @property
    def location_name(self):
        return self.get_location_name()

    @property
    def location_description(self):
        return self.get_location_description()
