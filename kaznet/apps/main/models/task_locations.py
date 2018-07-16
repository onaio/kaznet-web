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
    class Meta:
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
        """
        Get the location name
        """
        if self.location:
            return self.location.name
        return None

    def get_location_description(self):
        """
        Get the location description
        """
        if self.location:
            return self.location.description
        return None

    @property
    def location_name(self):
        """
        Model property to get the location name
        """
        return self.get_location_name()

    @property
    def location_description(self):
        """
        Model property to get the location description
        """
        return self.get_location_description()
